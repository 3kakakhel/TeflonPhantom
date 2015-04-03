%
% This script is used to fix up the image slices by using the method of
% replacing the deemed phantom values with the deemed average of 1920. It 
% is deemed that values 1575 or greater are that of the teflon in the
% phantom. Furthermore I remove random improperly unreplaced values by 
% testing if at least 7 of the adjacent values are properly replaced then
% replace the that pixel too.
% 

for k = 1:104 % Loop over each slice.

    % Read in the image slice.
    slicename = strcat('CT.1.2.826.0.1.3680043.2.200.209244332.186.6678.2849.',num2str(k),'.dcm');
    I = dicomread(slicename);

    % Read in the meta data.
    Imetadata = dicominfo(slicename);


    for j=1:512     % Loop over the columns.
        for i=1:512 % Loop over the rows.
            % Replace the teflon pixels.
            if (i>=252 & i<=256 & I(i,j)<=1575)           % If film position.
                % Do nothing                              % Do nothing.
            elseif (i>=238 & i<=244 & j>=253 & j<=260 & k>=46 & k<=60)    % If top chamber hole.
                I(i,j) = 1300;                                            % Make 1300
            elseif (i>=265 & i<=272 & j>=253 & j<=260 & k>=46 & k<=60)    % If bottom chamber hole.
                I(i,j) = 1300;                                            % Make 1300
            else
                if I(i,j) > 1575   % Test if the current value is teflon or not.
                    I(i,j) = 1920; % If it is then replace.
                end
            end
            
            % Fix isolated pixels.
            if (i == 1 || j == 1 || i == 512 || j == 512) % If on border.
                % Do nothing                              % Do nothing.
            elseif (i==254 || i==255 || i==256)           % If film position.
                % Do nothing                              % Do nothing.
            elseif (i>=238 & i<=244 & j>=253 & j<=260)    % If top chamber hole.
                % Do nothing                              % Do nothing.
            elseif (i>=265 & i<=272 & j>=253 & j<=260)    % If bottom chamber hole.
                % Do nothing                              % Do nothing.
            else
                if ( i==253 )            % If just above film position.
                    % Compute sum of adjacent 5 positions not on film
                    % position.
                    adjsum = I(i-1,j-1) + I(i-1,j) + I(i-1,j+1) + ...
                             I(i,j-1)   + I(i,j+1);
                    if (adjsum >= 5760)  % If 3+ around it are good pixels.
                        I(i,j) = 1920;   % Replace value.
                    end
                elseif ( i==257 )        % If just below film position.
                    % Compute sum of adjacent 5 positions not on film
                    % position.
                    adjsum = I(i,j-1) + I(i,j+1) + I(i+1,j-1) + ...
                                        I(i+1,j) + I(i+1,j+1);
                    if (adjsum >= 5760)  % If 3+ around it are good pixels.
                        I(i,j) = 1920;   % Replace value.
                    end
                else                     % If other positions.
                    % Compute the sum of the adjacent 8 elements.
                    adjsum = I(i-1,j-1) + I(i-1,j) + I(i-1,j+1) + ...
                             I(i,j-1)   + I(i,j+1) + I(i+1,j-1) + ...
                                          I(i+1,j) + I(i+1,j+1);
            
                    if (adjsum >= 13440) % If 6+ around it are good pixels.
                        I(i,j) = 1920;   % replace value.
                    end
                end
            end
        end
    end
    
    % Write a short progress note.
    fprintf('Finished slice %i of 104.\n', k);

    % Write the new image slice.
    dicomwrite(I, strcat('F:\TeflonPhantomOrig\replaced\',slicename), Imetadata);
end

%
%end
%