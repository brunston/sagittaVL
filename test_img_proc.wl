im = Import["https://i.imgur.com/WYixkT5.png"]
pv = PixelValuePositions[im, LightGray, 0.05]
highlighted = HighlightImage[im, pv, "HighlightColor" -> Yellow, Method -> {"DiskMarkers", 5}]
Export["test.jpg", highlighted, "JPEG"]
