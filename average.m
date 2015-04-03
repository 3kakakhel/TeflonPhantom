%
% This script is used to fix up the image slices by using the method of
% averaging all the pixels in the image with those around it but only if
% the difference between any of the adjacent pixels is <= 260. I do that so
% as to not mix the pixels for the phantom with those of the air or the 
% stand or film position or the ion chamber holes.
% 
 
for k = 1:104 % Loop over each slice.

    % Read in the image slice.
    slicename = strcat('CT.1.2.826.0.1.3680043.2.200.209244332.186.6678.2849.',num2str(k),'.dcm');
    I = dicomread(slicename);

    % Read in the meta data.
    Imetadata = dicominfo(slicename);

    for j=1:512     % Loop over the columns.
        for i=1:512 % Loop over the rows.
            if (i == 1 || j == 1 || i == 512 || j == 512) % If on the border
                I(i,j) = I(i,j);                   % Do nothing
            elseif (abs(I(i,j)-I(i-1,j)) <= 260 || ...% Test size of the difference
                    abs(I(i,j)-I(i,j-1)) <= 260 || ...
                    abs(I(i,j)-I(i-1,j-1)) <= 260 || ...
                    abs(I(i+1,j+1)-I(i,j)) <= 260 || ...
                    abs(I(i+1,j)-I(i,j)) <= 260 || ...
                    abs(I(i,j+1)-I(i,j)) <= 260 || ...
                    abs(I(i-1,j+1)-I(i,j)) <= 260 || ...
                    abs(I(i+1,j-1)-I(i,j)) <= 260)
                I(i,j) = I(i-1,j)   + I(i,j-1)   + I(i-1,j-1) + ...  % Do the sums
                         I(i+1,j+1) + I(i+1,j)   + I(i,j+1)   + ...
                                      I(i-1,j+1) + I(i+1,j-1);
                I(i,j) = I(i,j) / 8;                              % Divide to get the average and store
            end
        end
    end

    % Write a short progress note.
    fprintf('Finished slice %i of 104.\n', k);
    
    % Write the new image slice.
    dicomwrite(I, strcat('F:\TeflonPhantomOrig\averaged\',slicename), Imetadata);
end
    
%
%end
%