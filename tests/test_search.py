import importlib.util
import pathlib
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SEARCH_PATH = ROOT / "scripts" / "search.py"

spec = importlib.util.spec_from_file_location("mobile_search", SEARCH_PATH)
search_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_module)


class MobileNativeSearchTests(unittest.TestCase):
    def test_detect_domain_architecture(self):
        self.assertEqual(search_module.detect_domain("mvvm clean architecture"), "architecture")

    def test_domain_search_returns_results(self):
        result = search_module.search("mvvm viewmodel", "architecture", 2)
        self.assertEqual(result["domain"], "architecture")
        self.assertGreaterEqual(result["count"], 1)
        self.assertIn("name", result["results"][0])

    def test_all_domains_return_results(self):
        queries = {
            "ui-components": "bottom navigation tab bar card",
            "navigation-patterns": "stack navigation deep link drawer",
            "architecture": "mvvm clean architecture repository",
            "state-management": "stateflow viewmodel loading state",
            "performance": "startup memory rendering optimization",
            "testing": "unit test screenshot snapshot",
            "platform-apis": "camera location notification permission",
            "build-deployment": "play store fastlane signing version",
            "anti-patterns": "main thread network leak god activity",
        }

        for domain, query in queries.items():
            with self.subTest(domain=domain):
                result = search_module.search(query, domain, 2)
                self.assertEqual(result["domain"], domain)
                self.assertGreaterEqual(result["count"], 1)

    def test_stack_filtering(self):
        result = search_module.search_stack("android development", "kotlin", 3)
        self.assertEqual(result["stack"], "kotlin")
        self.assertGreaterEqual(result["count"], 1)
        self.assertTrue(all(row["stack"] == "kotlin" for row in result["results"]))

    def test_all_stacks_return_filtered_results(self):
        expected_stacks = {
            "kotlin",
            "swift",
            "compose",
            "swiftui",
            "flutter",
            "kmm",
            "room",
            "retrofit",
            "ktor",
            "hilt",
            "koin",
            "firebase",
        }
        self.assertTrue(expected_stacks.issubset(set(search_module.STACK_CONFIG.keys())))

        for stack in search_module.STACK_CONFIG:
            with self.subTest(stack=stack):
                result = search_module.search_stack("mobile development build deploy", stack, 5)
                self.assertEqual(result["stack"], stack)
                self.assertGreaterEqual(result["count"], 1)
                self.assertTrue(all(row["stack"] == stack for row in result["results"]))

    def test_architecture_output_contains_core_sections(self):
        output = search_module.generate_architecture(
            "e-commerce android kotlin compose",
            "ShopApp",
        )
        self.assertIn("TARGET:", output)
        self.assertIn("ARCH:", output)
        self.assertIn("AVOID:", output)
        self.assertIn("CHECKLIST:", output)

    def test_persist_architecture_writes_master(self):
        temp_dir = pathlib.Path(ROOT, "test-output", "persist")
        temp_dir.mkdir(parents=True, exist_ok=True)
        output = search_module.persist_architecture(
            "kotlin compose mvvm",
            project_name="Test App",
            output_dir=str(temp_dir),
        )
        master = temp_dir / "architecture" / "test-app" / "MASTER.md"
        self.assertTrue(master.exists())
        self.assertIn("Persisted Files", output)

    def test_cli_list_when_node_available(self):
        if shutil.which("node") is None:
            self.skipTest("Node.js is not available")

        cli = ROOT / "cli" / "bin" / "mobile-native-pro-max.js"
        result = subprocess.run(
            ["node", str(cli), "list"],
            cwd=str(ROOT.parent),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex", result.stdout)


if __name__ == "__main__":
    unittest.main()
