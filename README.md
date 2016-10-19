# imgDL
Python script for downloading images

*imgDL* is a beginner-created python script for downloading images off given URLs. 

**How it works**
Given a valid URL (with http://), imgDL retrieves all `<img>` `src` attributes, as well as `href` `<a>` attributes (given that they link to a url ending with .jpg, .jpeg, or .png. The images are then saved to the working directory.

Supported URLs will yield more optimised downloads. (e.g. links to 4chan threads will skip all thumbnails to instead download the source images)

**Dependencies**
- requests
- beautifulsoup

**Supported URLs**
- [x] http://boards.4chan.org/*board*/thread/*threadnumber*/*threadname*
- [ ] reddit
- [x] universal (all img tags)

**Bugs**
- [X] *(Fixed!)* Universal mode only works sometimes, since different sites reference URLs in their img tags differently.
