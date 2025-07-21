from dataclasses import dataclass
from pathlib import Path
import sys
from os import environ

PROJECT_DIR = Path(__file__).parent

SOAR_RELEASE_VERSION = environ.get("SOAR_RELEASE_VERSION")

SOAR_SHUFFLER_DIR = PROJECT_DIR / "SoarShuffler"

SOAR_SHUFFLER_OUTPUT_DIR = SOAR_SHUFFLER_DIR / f"Soar-Release-{SOAR_RELEASE_VERSION}"


def get_required_env_var_path(name):
    if p := environ.get(name):
        return Path(p)
    else:
        raise ValueError(f"{name} is not set")


SOAR_GROUP_REPOS_HOME = get_required_env_var_path("SOAR_GROUP_REPOS_HOME")
SOAR_WIN_X86_64_COMPILED_DIR = get_required_env_var_path("SOAR_WIN_X86_64_COMPILED_DIR")
SOAR_WIN_X86_64_COMPILED_DIR = get_required_env_var_path("SOAR_WIN_X86_64_COMPILED_DIR")
SOAR_LINUX_X86_64_COMPILED_DIR = get_required_env_var_path(
    "SOAR_LINUX_X86_64_COMPILED_DIR"
)
SOAR_MAC_X86_64_COMPILED_DIR = get_required_env_var_path("SOAR_MAC_X86_64_COMPILED_DIR")
SOAR_MAC_ARM64_COMPILED_DIR = get_required_env_var_path("SOAR_MAC_ARM64_COMPILED_DIR")


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
    print(
        (
            f"Step {step.value}: Update version numbers in Soar everywhere. See example_version_bump.patch, or "
            "for an internal release (.a1, .a2, etc.) see example_internal_version_update.patch. "
            "Then push the changes so that Soar is rebuilt with the correct version info."
        )
    )
    step.proceed()

    print(f"Step {step.value}: Update version numbers in txt/README.md.")
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
            f"Step {step.value}: Add some cursory release notes in txt/README.md. "
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

def update_manual_version(step: Step):
    print(
        (
            f"Step {step.value}: Update the manual version in the website repository: https://github.com/SoarGroup/SoarGroup.github.io, under docs/soar_manual/template.tex. "
            "Push your changes and allow the PDF build to complete."
        )
    )
    step.proceed()

def manual_pdf(step: Step):
    print(
        (
            f"Step {step.value}: Grab the latest SoarManual build from the website's "
            "build_pdf action "
            "(https://github.com/SoarGroup/SoarGroup.github.io/actions/workflows/build_pdf.yml) "
            "and place it in pdf/SoarManual.pdf in this repository."
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
            " Then rename VisualSoar/build/libs/VisualSoar-<version>.jar without the version number."
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
        (
            SOAR_GROUP_REPOS_HOME
            / "VisualSoar"
            / "build"
            / "libs"
            / "VisualSoar.jar"
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
        "jackson-annotations-2.18.2.jar",
        "jackson-core-2.18.2.jar",
        "jackson-databind-2.18.2.jar",
    ]
    print(
        f"Step {step.value}: Gather the following JARs from the various Java projects and place them under SoarShuffler/jars. The jackson JARs specifically are in the VisualSoar repo.\n"
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
            " - Be sure that the env vars we checked in step 1) are still correctly loaded.\n"
            " - python3 soar_shuffler.py Soar_Projects_Filelist.txt\n"
            "The script will tell you if it can't find any files that it needs. You'll probably need to run it "
            "a couple of times to hunt down all of the files you need. You'll probably want to `rm -rf SoarSuite` "
            "between runs, just to make sure you aren't keeping any old files in the release."
        )
    )
    step.proceed(
        check_function=lambda: (
            SOAR_SHUFFLER_OUTPUT_DIR
            / f"SoarSuite_{SOAR_RELEASE_VERSION}-Multiplatform.zip"
        ).resolve(strict=True)
    )


def inspect_release(step: Step):
    print(
        (
            f"Step {step.value}: Unzip SoarShuffler/Soar-Release-{SOAR_RELEASE_VERSION}/Soar_{SOAR_RELEASE_VERSION}-Multiplatform.zip "
            "and ensure everything is in order. Check that VisualSoar, the debugger, TankSoar, and SoarCLI all work with a simple double-click. "
            "Test on Mac (Intel and ARM), Windows, and Linux."
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
            f"Type 'releases/{SOAR_RELEASE_VERSION} into the tag field and select 'Create new tag'. "
            "Copy the basic change notes from txt/README.md to the description and upload "
            f"Soar_{SOAR_RELEASE_VERSION}-Multiplatform.zip, and all of the documentation PDFs. "
            "Leave 'Set as a pre-release' *unchecked*, 'Set as the latest release' *checked* and hit 'Publish release'."
        )
    )
    step.proceed()

def ensure_pypi_release(step: Step):
    print(
        (
            f"Step {step.value}: Check that the release triggered the pypi publication workflow (GH Action), "
            "and that it finished successfully. If there are errors, you can fix the issue in the repo code "
            "and re-trigger the workflow from the Actions UI on GitHub."
        )
    )
    step.proceed()



def commit_downloads(step: Step):
    print(
        (
            f"Step {step.value}: Commit the various generated zip files to the SoarGroup/website-downloads repo "
            f"(except for Soar_{SOAR_RELEASE_VERSION}-Multiplatform.zip). "
            "It's likely that nothing here will have changed."
        )
    )
    step.proceed()


def update_website(step: Step):
    print(
        (
            f"Step {step.value}: Update the website with the new release information: https://github.com/SoarGroup/SoarGroup.github.io. "
            "This includes adding a release announcement and updating soar_version (which updates download links for the manual and tutorial), "
            "as well as updating the release notes on the 'latest' download page."
        )
    )
    step.proceed()


def announce_on_mailing_list(step: Step):
    print(
        (
            f"Step {step.value}: Announce the release on the Soar mailing list: soar-cognitive-architecture@googlegroups.com. "
            "Include a link to the release notes and a brief description of the changes."
        )
    )
    step.proceed()


def git_tag(step: Step):
    print(
        (
            f"Step {step.value}: Push {SOAR_RELEASE_VERSION} tags for Release-Support, VisualSoar, SoarGroup.github.io, and website-downloads."
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
    update_manual_version(step_counter)
    manual_pdf(step_counter)
    download_builds(step_counter)
    build_visual_soar(step_counter)
    build_eaters_tanksoar(step_counter)
    gather_jars(step_counter)
    run_soar_shuffler(step_counter)
    inspect_release(step_counter)
    upload_to_github(step_counter)
    ensure_pypi_release(step_counter)
    commit_downloads(step_counter)
    update_website(step_counter)
    announce_on_mailing_list(step_counter)
    git_tag(step_counter)

    print("Release complete! 🎊🥳🥂, 😪🛌😴")


if __name__ == "__main__":
    main(sys.argv[1:])
