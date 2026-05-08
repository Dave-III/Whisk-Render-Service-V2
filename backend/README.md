# Whisk Render Service

A backend rendering service for the game *Whisk* that automatically combines two player POV clips into a single synchronized speedrun video and uploads the result to YouTube.

The service supports:

* MP4 uploads
* Medal.tv clip URLs
* Automatic video composition
* YouTube uploads
* REST API integration

Designed for easy integration into leaderboard and speedrun submission workflows.

Client → API → Renderer → YouTube → URL

## MVP Goals

- [x] Accept two MP4 uploads
- [x] Accept Medal.tv clip URLs
- [x] Render side-by-side output
- [x] Downloadable Renders
- [x] Side-by-side composition
- [x] Modular rendering service
- [x] Upload final video to YouTube
- [x] Return public/unlisted URL

## Future Projects
- [ ] Docker deployment
