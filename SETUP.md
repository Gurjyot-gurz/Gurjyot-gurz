# Setup — Gurjyot's GitHub profile

1. Create a **public** repository named exactly `Gurjyot-gurz` (same as your GitHub username). If it already exists, back up its current README first.
2. Copy the contents of this kit into that repository's root, preserving the folders: `README.md`, `.github/workflows/profile-activity.yml`, `scripts/render_profile.py`, and `assets/profile/`.
3. Open **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, and save.
4. Open **Actions → Refresh GitHub profile cards → Run workflow**. After it succeeds, the SVG cards will appear in the README.
5. The workflow refreshes contribution cards daily at 05:30 UTC. Your PC does not need to be on.

Notes:
- The workflow uses the built-in `GITHUB_TOKEN`; do not create or paste a personal access token.
- Contribution totals come from GitHub's contribution calendar. Private contribution visibility follows your GitHub profile settings; private repository details are not exposed.
- The README cannot run JavaScript or custom page CSS. SVG images provide the visual cards and lightweight animation.
- Featured project names reflect projects you've previously discussed. Add exact repository links for TalentFlow, AutoScale Shop, Serverless Identity Verification Pipeline, and Minecraft Infrastructure & DevOps Platform; remove any that are not public or ready to showcase.
