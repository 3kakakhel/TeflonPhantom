%
% Collect all the slices into a single array and save as a txt file.
%

% Make a master array.
M = zeros(512, 512, 118);

for k = 1:118 % Loop over each slice.

    % Read in the image slice.
    slicename = strcat('CT.1.2.826.0.1.3680043.2.200.1576685169.411.32303.2849.',num2str(k),'.dcm');
    Io = dicomread(strcat('.\Orig\',slicename));
    Ir = dicomread(strcat('.\m3\',slicename));

    % Store the original slice
    O(:,:,k) = Io;
    
    % Store the replaced slice
    R(:,:,k) = Ir;        
end

% Save both arrays
save OR.mat O R