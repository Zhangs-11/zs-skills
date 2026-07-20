import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "generate_wechat_images.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("generate_wechat_images", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["generate_wechat_images"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GenerateImagesScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self._siliconflow_key = os.environ.pop("SILICONFLOW_API_KEY", None)

    def tearDown(self) -> None:
        if self._siliconflow_key is not None:
            os.environ["SILICONFLOW_API_KEY"] = self._siliconflow_key

    def test_extracts_image_requests_from_markdown_placeholders(self) -> None:
        script = load_script_module()
        md = (
            "正文\n\n"
            "[插图：传统RAG工作流]\n"
            "[绘图提示：A clean technical diagram of a RAG pipeline]\n"
        )

        requests = script.extract_image_requests(md)

        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].description, "传统RAG工作流")
        self.assertEqual(requests[0].prompt, "A clean technical diagram of a RAG pipeline")
        self.assertEqual(requests[0].filename, "01-rag.jpg")

    def test_replaces_placeholders_with_relative_markdown_image_paths(self) -> None:
        script = load_script_module()
        md = (
            "正文\n\n"
            "[插图：架构图]\n"
            "[绘图提示：A clean architecture diagram]\n"
        )
        request = script.ImageRequest(
            description="架构图",
            prompt="A clean architecture diagram",
            filename="01-image.jpg",
            placeholder="[插图：架构图]\n[绘图提示：A clean architecture diagram]",
        )

        result = script.replace_placeholders(md, [request], Path("images"))

        self.assertIn("![架构图](images/01-image.jpg)", result)
        self.assertNotIn("[插图：", result)

    def test_builds_siliconflow_payload(self) -> None:
        script = load_script_module()

        payload = script.build_generation_payload("prompt", image_size="1024x1024")

        self.assertEqual(payload["model"], "Tongyi-MAI/Z-Image-Turbo")
        self.assertEqual(payload["prompt"], "prompt")
        self.assertEqual(payload["image_size"], "1024x1024")

    def test_writes_updated_markdown_after_generation(self) -> None:
        script = load_script_module()
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp) / "article.md"
            article.write_text(
                "正文\n\n[插图：架构图]\n[绘图提示：A clean architecture diagram]\n",
                encoding="utf-8",
            )
            calls = []

            def fake_generate(prompt, output_path, **kwargs):
                calls.append((prompt, output_path))
                output_path.write_bytes(b"png")

            script.generate_article_images(
                article,
                title="AI文章",
                generator=fake_generate,
            )

            updated = article.read_text(encoding="utf-8")
            cover = Path(tmp) / "images" / "article" / "cover.jpg"
            cover_exists = cover.exists()

        self.assertIn("![架构图](images/article/01-image.jpg)", updated)
        self.assertTrue(calls[0][1].name == "01-image.jpg")
        self.assertTrue(calls[1][1].name == "cover.jpg")
        self.assertTrue(cover_exists)

    def test_auto_inserts_images_when_article_has_no_placeholders(self) -> None:
        script = load_script_module()
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp) / "article.md"
            article.write_text(
                "# RAG切分为什么会翻车\n\n"
                "第一段解释问题背景，说明chunk切分会破坏上下文。\n\n"
                "第二段讲parent-child retrieval如何工作，小块负责召回，大块负责阅读。\n\n"
                "第三段总结工程取舍，说明不同文档需要不同策略。\n",
                encoding="utf-8",
            )
            calls = []

            def fake_generate(prompt, output_path, **kwargs):
                calls.append((prompt, output_path))
                output_path.write_bytes(b"png")

            script.generate_article_images(
                article,
                title="RAG切分为什么会翻车",
                generator=fake_generate,
                auto_insert=2,
            )

            updated = article.read_text(encoding="utf-8")

        self.assertIn("![配图1](images/article/01-image.jpg)", updated)
        self.assertIn("![配图2](images/article/02-image.jpg)", updated)
        self.assertTrue(calls[0][1].name == "01-image.jpg")
        self.assertTrue(calls[1][1].name == "02-image.jpg")
        self.assertTrue(calls[2][1].name == "cover.jpg")

    def test_spread_indexes_returns_each_available_position(self) -> None:
        script = load_script_module()

        self.assertEqual(script._spread_indexes([0, 2], 2), [0, 2])

    def test_auto_insert_is_idempotent_when_generated_images_exist(self) -> None:
        script = load_script_module()
        md = (
            "第一段正文内容足够长，可以用于自动插入配图。\n\n"
            "![配图1](images/article/01-image.png)\n\n"
            "第二段正文内容同样足够长，可以用于自动插入配图。\n"
        )

        updated, requests = script.auto_insert_image_requests(md, count=2)

        self.assertEqual(updated, md)
        self.assertEqual(requests, [])

    def test_rerun_does_not_append_after_explicit_placeholder_generation(self) -> None:
        script = load_script_module()
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp) / "article.md"
            original = (
                "正文第一段足够长，用来说明文章的主要背景。\n\n"
                "![Architecture](images/article/01-architecture.jpg)\n\n"
                "正文第二段同样足够长，用来继续说明文章结论。\n"
            )
            article.write_text(original, encoding="utf-8")
            calls = []

            def fake_generate(prompt, output_path, **kwargs):
                calls.append(output_path)
                output_path.write_bytes(b"jpg")

            script.generate_article_images(
                article,
                title="文章标题",
                generator=fake_generate,
                auto_insert=3,
            )

            self.assertEqual(article.read_text(encoding="utf-8"), original)
            self.assertEqual([path.name for path in calls], ["cover.jpg"])

    def test_legacy_flat_image_layout_is_also_idempotent(self) -> None:
        script = load_script_module()
        md = (
            "正文第一段足够长，用来说明文章的主要背景。\n\n"
            "![Architecture](images/01-architecture.jpg)\n\n"
            "正文第二段同样足够长，用来继续说明文章结论。\n"
        )

        updated, requests = script.auto_insert_image_requests(md, count=3)

        self.assertEqual(updated, md)
        self.assertEqual(requests, [])

    def test_non_prose_blocks_are_not_image_candidates(self) -> None:
        script = load_script_module()

        self.assertFalse(script._is_content_paragraph("```python\nprint('long enough')\n```"))
        self.assertFalse(script._is_content_paragraph("> 一段很长的引用内容，不应该成为自动配图锚点。"))
        self.assertFalse(script._is_content_paragraph("| 字段 | 一段很长的表格内容 |"))
        self.assertFalse(script._is_content_paragraph("![配图](images/article/01-image.png)"))
        self.assertFalse(script._is_content_paragraph("> / 作者：卡卡罗特，这里是固定尾部信息。"))

    def test_cover_prompt_uses_title_and_custom_api_base(self) -> None:
        script = load_script_module()
        captured = {}

        def fake_summarize(theme, api_key, api_base):
            captured["theme"] = theme
            captured["api_base"] = api_base
            return "a bright bridge connecting two computing worlds"

        with patch.object(script, "_summarize_concept_en", side_effect=fake_summarize):
            script._cover_prompt(
                "K3真的把Claude拉下王座了吗？",
                "昨晚，一个前端榜单换王了。",
                api_key="test-key",
                api_base="https://example.invalid/v1",
            )

        self.assertIn("K3真的把Claude拉下王座了吗？", captured["theme"])
        self.assertEqual(captured["api_base"], "https://example.invalid/v1")

    def test_cover_failure_does_not_modify_article(self) -> None:
        script = load_script_module()
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp) / "article.md"
            original = "正文\n\n[插图：架构图]\n[绘图提示：A clean architecture diagram]\n"
            article.write_text(original, encoding="utf-8")

            def fail_on_cover(prompt, output_path, **kwargs):
                if output_path.name == "cover.jpg":
                    raise RuntimeError("cover generation failed")
                output_path.write_bytes(b"png")

            with self.assertRaisesRegex(RuntimeError, "cover generation failed"):
                script.generate_article_images(
                    article,
                    title="文章标题",
                    generator=fail_on_cover,
                )

            self.assertEqual(article.read_text(encoding="utf-8"), original)

    def test_invalid_download_does_not_replace_existing_image(self) -> None:
        script = load_script_module()

        class GenerationResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return b'{"images": [{"url": "https://example.com/image.png"}]}'

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "image.jpg"
            output.write_bytes(b"existing-image")
            with (
                patch.object(
                    script.urllib.request,
                    "urlopen",
                    return_value=GenerationResponse(),
                ),
                patch.object(
                    script,
                    "download_public_url",
                    return_value=unittest.mock.MagicMock(body=b"not-an-image"),
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "valid image"):
                    script.generate_one_image("prompt", output, api_key="test-key")

            self.assertEqual(output.read_bytes(), b"existing-image")

    def test_generated_image_private_url_is_rejected(self) -> None:
        script = load_script_module()

        class GenerationResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return b'{"images": [{"url": "https://127.0.0.1/image.png"}]}'

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "image.jpg"
            with (
                patch.object(
                    script.urllib.request,
                    "urlopen",
                    return_value=GenerationResponse(),
                ),
                patch.object(
                    script,
                    "download_public_url",
                    side_effect=script.SecureDownloadError(
                        "remote image points to a private or local address"
                    ),
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "private or local"):
                    script.generate_one_image("prompt", output, api_key="test-key")


if __name__ == "__main__":
    unittest.main()
