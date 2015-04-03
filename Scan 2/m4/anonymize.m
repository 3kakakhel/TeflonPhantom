s = 65;

I=dicomread(slicename);
Imetadata = dicominfo(slicename);

values.SeriesNumber = 253215347;
values.StudyInstanceUID = dicomuid;
values.SeriesInstanceUID = dicomuid;
values.FrameOfReferenceUID = dicomuid;

for s=1:124
    slicename=strcat('CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.',num2str(s),'.dcm');
    dicomanon(strcat('.\',slicename),strcat('.\m4a\',slicename),'update',values);
end