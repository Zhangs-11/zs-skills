import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


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
        self.assertEqual(requests[0].filename, "01-rag.png")

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
            filename="01-image.png",
            placeholder="[插图：架构图]\n[绘图提示：A clean architecture diagram]",
        )

        result = script.replace_placeholders(md, [request], Path("images"))

        self.assertIn("![架构图](images/01-image.png)", result)
        self.assertNotIn("[插图：", result)

    def test_builds_siliconflow_payload(self) -> None:
        script = load_script_module()

        payload = script.build_generation_payload("prompt", image_size="1024x1024")

        self.assertEqual(payload["model"], "stabilityai/stable-diffusion-xl-base-1.0")
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
            cover = Path(tmp) / "images" / "cover.png"
            cover_exists = cover.exists()

        self.assertIn("![架构图](images/01-image.png)", updated)
        self.assertTrue(calls[0][1].name == "01-image.png")
        self.assertTrue(calls[1][1].name == "cover.png")
        self.assertTrue(cover_exists)


if __name__ == "__main__":
    unittest.main()
