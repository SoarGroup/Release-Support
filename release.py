from dataclasses import dataclass
from pathlib import Path
import sys
from os import environ

PROJECT_DIR = Path(__file__).parent

SOAR_RELEASE_VERSION = environ.get("SOAR_RELEASE_VERSION")

SOAR_SHUFFLER_DIR = PROJECT_DIR / "SoarShuffler"

SOAR_SHUFFLER_OUTPUT_DIR = SOAR_SHUFFLER_DIR / f"Soar-Release-{SOAR_RELEASE_VERSION}"

SOAR_GROUP_REPOS_HOME = Path(environ.get("SOAR_GROUP_REPOS_HOME"))

SOAR_WIN_X86_64_COMPILED_DIR = Path(environ.get("SOAR_WIN_X86_64_COMPILED_DIR"))
SOAR_LINUX_X86_64_COMPILED_DIR = Path(environ.get("SOAR_LINUX_X86_64_COMPILED_DIR"))
SOAR_MAC_X86_64_COMPILED_DIR = Path(environ.get("SOAR_MAC_X86_64_COMPILED_DIR"))
SOAR_MAC_ARM64_COMPILED_DIR = Path(environ.get("SOAR_MAC_ARM64_COMPILED_DIR"))


@dataclass
class Step:
    value: int = 1

    def proceed(self, confirm=True, check_function=None, fail_message=None):
        self.value += 1
        if confirm:
            input("Press [Enter] to continue...")
            if check_function:
                passed = False
                while not passed:
                    try:
                        check_function()
                        passed = True
                        print("✅ Check passed")
                    except Exception as e:
                        print(e)
                        print("❌ Check failed!")
                        if fail_message:
                            print(fail_message)
                        input("Press [Enter] to re-try check...")
        print()


def report_vars(step: Step):
    print(f"Step {step.value}: Confirm following variables:")
    print(f"{SOAR_RELEASE_VERSION=}")
    print(f"{SOAR_SHUFFLER_OUTPUT_DIR=}")
    print(f"{SOAR_GROUP_REPOS_HOME=}")
    print(f"{SOAR_WIN_X86_64_COMPILED_DIR=}")
    print(f"{SOAR_LINUX_X86_64_COMPILED_DIR=}")
    print(f"{SOAR_MAC_X86_64_COMPILED_DIR=}")
    print(f"{SOAR_MAC_ARM64_COMPILED_DIR=}")
    step.proceed()


def export_tutorial(step: Step):
    print(
        f"Step {step.value}: Manually export changes to SoarTutorial/*.docx from Word to pdf/"
    )
    step.proceed()


def bump_version(step: Step):
    # TODO: manual source will be unified with website version in the future.
    print(
        (
            f"Step {step.value}: Update version number in ManualSource/manual.tex (look for 'SoarVersionRevision'). "
            "Then push the changes so that the manual is rebuilt. "
        )
    )
    step.proceed()

    print(
        (
            f"Step {step.value}: Update version numbers in Soar everywhere (see example_version_bump.patch). "
            "Then push the changes so that Soar is rebuilt with the correct version info."
        )
    )
    step.proceed()

    print(f"Step {step.value}: Update version numbers in txt/README.")
    step.proceed()


def release_notes(step: Step):
    release_notes_file = (
        PROJECT_DIR / "txt" / f"Release_Notes_{SOAR_RELEASE_VERSION}.md"
    )
    print(
        (
            f"Step {step.value}: Create and fill {release_notes_file} using a previous release notes file as a template. "
            "Ensure full correctness of file."
        )
    )
    step.proceed(check_function=lambda: release_notes_file.resolve(strict=True))

    print(
        (
            f"Step {step.value}: Add some cursory release notes in txt/README. "
            "Ensure full correctness of file."
        )
    )
    step.proceed()


def build_instructions(step: Step):
    print(
        f"Step {step.value}: Ensure build instructions in txt/Building_Soar.md are up-to-date."
    )
    step.proceed()


def clone_repos(step: Step):
    print(
        f"Step {step.value}: Clone the necessary SoarGroup repositories to {SOAR_GROUP_REPOS_HOME}"
    )

    def check():
        SOAR_GROUP_REPOS_HOME.resolve(strict=True)
        required_repos = [
            "Other-Agent-Development-Tools",
            "Domains-SoarQnA",
            "Domains-SoarTextIO",
            "Domains-WordNet",
            "Domains-WordNet-with-Parse-Trees",
            "Examples-and-Unsupported",
            "Domains-RoomsWorld",
            "Domains-InfiniteMario",
            "Domains-DiceQnA",
            "Domains-Dice",
            "Domains-General-Game-Playing",
            "Domains-Planning-Domain-Definition-Language",
            "Agents",
            "Domains-Eaters-TankSoar",
            "VisualSoar",
        ]
        for repo in required_repos:
            repo_path = SOAR_GROUP_REPOS_HOME / repo
            repo_path.resolve(strict=True)

    step.proceed(check_function=check)


def manual_pdf(step: Step):
    print(
        (
            f"Step {step.value}: Grab the latest manual build from this "
            "repository's GH Actions artifacts and place it in pdf/."
        )
    )
    step.proceed()


def download_builds(step: Step):
    print(
        (
            f"Step {step.value}: Download the latest Soar builds from the Soar repo's GH Actions artifacts. "
            "They should be unzipped and placed in the directories specified above for "
            "SOAR_WIN_X86_64_COMPILED_DIR, SOAR_LINUX_X86_64_COMPILED_DIR, "
            "SOAR_MAC_X86_64_COMPILED_DIR, and SOAR_MAC_ARM64_COMPILED_DIR."
        )
    )

    def check():
        SOAR_WIN_X86_64_COMPILED_DIR.resolve(strict=True)
        SOAR_LINUX_X86_64_COMPILED_DIR.resolve(strict=True)
        SOAR_MAC_X86_64_COMPILED_DIR.resolve(strict=True)
        SOAR_MAC_ARM64_COMPILED_DIR.resolve(strict=True)

    step.proceed(check_function=check)


def build_visual_soar(step: Step):
    print(f"Step {step.value}: Build VisualSoar")
    step.proceed()

    print(
        (
            f"Step {step.value}: Convert VisualSoar's manual to pdf; if on Mac, do this:"
            "  - `brew install basictex`"
            "  - open new shell"
            "  - `sudo tlmgr install soul`"
            "  - `cd VisualSoar/doc/usersman`"
            "  - `pandoc -o VisualSoar_UsersManual.pdf VisualSoar_UsersManual.docx`"
        )
    )

    def check():
        (
            SOAR_GROUP_REPOS_HOME
            / "VisualSoar"
            / "doc"
            / "usersman"
            / "VisualSoar_UsersManual.pdf"
        ).resolve(strict=True)

    step.proceed(check_function=check)


def build_eaters_tanksoar(step: Step):
    print(
        f"Step {step.value}: Build Eaters_TankSoar.jar and place it under SoarShuffler/jars."
    )
    step.proceed(
        check_function=lambda: (
            SOAR_SHUFFLER_DIR / "jars" / "Eaters_TankSoar.jar"
        ).resolve(strict=True)
    )


def gather_jars(step: Step):
    required_jars = [
        "commons-logging-1.1.1.jar",
        "log4j-1.2.15.jar",
        "stopwatch-0.4-with-deps.jar",
    ]
    print(
        f"Step {step.value}: Gather the following jar's under SoarShuffler/jars:\n"
        + "\n".join(map(lambda j: f" - {j}", required_jars))
    )

    def check():
        for j in required_jars:
            (SOAR_SHUFFLER_DIR / "jars" / j).resolve(strict=True)

    step.proceed(check_function=check)


def run_soar_shuffler(step: Step):
    print(
        (
            f"Step {step.value}: Run SoarShuffler:\n"
            " - cd SoarShuffle\n"
            " - python3 soar_shuffler.py Soar_Projects_Filelist.txt\n"
            "The script will tell you if it can't find any files that it needs. You'll probably need to run it "
            "a couple of times to hunt down all of the files you need. You'll probably want to `rm -rf SoarSuite` "
            "between runs, just to make sure you aren't keeping any old files in the release."
        )
    )
    step.proceed(check_function=lambda: SOAR_SHUFFLER_OUTPUT_DIR.resolve(strict=True))


def inspect_release(step: Step):
    print(
        (
            f"Step {step.value}: Unzip SoarShuffler/Soar-Release-{SOAR_RELEASE_VERSION}/Soar_{SOAR_RELEASE_VERSION}-Multiplatform.zip "
            "and ensure everything is in order. Check that VisualSoar, the debugger, TankSoar, and SoarCLI all work with a simple double-click."
        )
    )
    step.proceed()

    print(
        f"Step {step.value}: Share the release with others and get feedback. Repeat this whole process if necessary."
    )
    step.proceed()


def upload_to_github(step: Step):
    print(
        (
            f"Step {step.value}: Create a new release on GitHub: https://github.com/SoarGroup/Soar/releases/new. "
            f"Type 'releases/{SOAR_RELEASE_VERSION} into the tag field and select 'Create new tag'."
            "Copy the basic change notes from txt/README to the description and upload "
            f"Soar_{SOAR_RELEASE_VERSION}-Multiplatform.zip and all of the documentation PDFs."
            "Leave 'Set as a pre-release' *unchecked*, 'Set as the latest release' *checked* and hit 'Publish release'."
        )
    )
    step.proceed()


def git_tag(step: Step):
    print(
        (
            f"Step {step.value}: Push {SOAR_RELEASE_VERSION} tags for Release-Support and VisualSoar."
        )
    )
    step.proceed()


def update_website(step: Step):
    print(
        (
            f"Step {step.value}: Update the website with the new release information: https://github.com/SoarGroup/SoarGroup.github.io. "
            "This includes adding a release announcement and updating download links for the manual and tutorial."
        )
    )
    step.proceed()


def main(args):
    step_counter = Step()
    report_vars(step_counter)
    export_tutorial(step_counter)
    bump_version(step_counter)
    release_notes(step_counter)
    clone_repos(step_counter)
    manual_pdf(step_counter)
    download_builds(step_counter)
    build_visual_soar(step_counter)
    build_eaters_tanksoar(step_counter)
    gather_jars(step_counter)
    run_soar_shuffler(step_counter)
    inspect_release(step_counter)


if __name__ == "__main__":
    main(sys.argv[1:])
