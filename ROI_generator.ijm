//specify the location of the folder that contains the images
in_dir = "/hard drive/image directory/";
//specify the location of the folder to save ROIs
out_dir = "/hard drive/image directory/ROIs/";
//Set to hide active images for increasing computational rapidity
setBatchMode("hide");
//input the minimum cell area. Any thresholded objects below this threshold are filtered out.
min_cell_area = 100
//Acquire directory information
	img_list = getFileList(in_dir);
	for(i=0; i < img_list.length; i++) {
			open(in_dir + "/" + img_list[i]);
			setAutoThreshold("Minimum dark");
			run("Threshold...");
			setOption("BlackBackground", false);
			run("Convert to Mask");
			run("Close");
			run("Analyze Particles...", "size=min_cell_area-Infinity  show=Outlines display clear summarize add in_situ");
			run("Select All");
			roiManager("Save", out_dir+"\\"+img_list[i]+".zip");
			roiManager("Delete");
			run("Close All");}
	//}