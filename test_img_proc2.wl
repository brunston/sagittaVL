(* ::Package:: *)

Do [im = Import[StringJoin[ToString[i],".png"]];
pv = PixelValuePositions[im, LightGray, 0.05];
highlighted = HighlightImage[im, pv, "HighlightColor" -> Yellow, Method -> {"DiskMarkers", 5}];
Export[StringJoin["test", ToString[i], ".jpg"], highlighted, "JPEG"],
{i, 1, 3, 1}]



Import[StringJoin[ToString[1],".png"]]
Do[Print[i], {i, 1, 3, 1}]



