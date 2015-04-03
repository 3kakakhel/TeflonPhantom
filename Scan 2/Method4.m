% 0. Store all pixel values into a 3d array.
% 1. Determine the mean and std of all pixel values that could be the phantom,
%    namely those that are above Pcut which is deemed to be 1650 for now.
%    Rather than use all pixels from all slices, I just use a
%    representative slice, namely slice 60.
% 2. Replace all pixels in the range  mean +/- 3 std  by the mean.


fprintf('____________\n|\n| Start\n|___________\n\n');


% Define the representative phantom slice.
Prep = 65;
Irep = zeros(512,512);


fprintf('Read in, average, and store all the pixel values.\n');
for k=1:124
    slicename = strcat('CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.',num2str(k),'.dcm');
    I = dicomread(strcat('.\',slicename));
    Imetadata = dicominfo(strcat('.\',slicename));
    for j=2:511
        for i=2:511
            if (abs(I(i,j)-I(i-1,j)) <= 260 || ...% Test size of the difference
                abs(I(i,j)-I(i,j-1)) <= 260 || ...
                abs(I(i,j)-I(i-1,j-1)) <= 260 || ...
                abs(I(i+1,j+1)-I(i,j)) <= 260 || ...
                abs(I(i+1,j)-I(i,j)) <= 260 || ...
                abs(I(i,j+1)-I(i,j)) <= 260 || ...
                abs(I(i-1,j+1)-I(i,j)) <= 260 || ...
                abs(I(i+1,j-1)-I(i,j)) <= 260)
                A = I(i-1,j)   + I(i,j-1)   + I(i-1,j-1) + ...  % Compute sum of adjacent 8 pixels
                    I(i+1,j+1) + I(i+1,j)   + I(i,j+1)   + ...
                                 I(i-1,j+1) + I(i+1,j-1);
                I(i,j) = A / 8;                                     % Divide to get the average and store
            end
            if k==Prep
                Irep(i,j) = I(i,j);
            end
        end
    end
    dicomwrite(I, strcat('.\m4\',slicename), Imetadata);
    
    % Write a short progress note.
    fprintf('Finished slice %i of 124.\n', k);
    
    if k==Prep
        plot(ind,Irep(:,200:300),ind,double(Pavg)*ones(1,512),ind,double(Pcut)*ones(1,512),ind,double(Pavg-2*Pstd)*ones(1,512));
    end
end


fprintf('Determining the cutoff value.\n');
Pprev = 0;
i = 0;                                      % Which iteration are we on?
upper = max(max(Irep)');                    % Define upper bound.
lower = 0;                                  % Define lower bound.
toCont = 1;
Pcut = uint16((upper+lower)*3/4);           % Define the initial guess.
A = [];                                     % Array to hold all values above the cutoff.
l = 1;
for c=1:512
    for r=1:512
        if Irep(r,c)>=Pcut
            A(l) = Irep(r,c);
            l = l + 1;
        end
    end
end
Aavg = uint16(mean(A));                     % Store mean of values above cutoff.
Astd = uint16(std(A));                      % Store std  of values above cutoff.
fprintf('    Aavg = %i   Astd = %i\n',Aavg,Astd);
while toCont    
    fprintf('Performing iteration %i. Current guess: Pcut = %i\n',i,Pcut);    % Display progress.
    Pcut = uint16((upper+lower)/2);
    if Pcut == Pprev
        toCont = 0;
    elseif Pcut > (Aavg-2*Astd)
        upper = Pcut;
    elseif Pcut < (Aavg-2*Astd)
        lower = Pcut;
    else
        toCont = 0;
    end
    i = i + 1;
    Pprev = Pcut;
end


% Determine the average and std of all values Pcut or higher in the representative slice.
Pabv = [];
l = 1;
fprintf('Computing the mean and std of phantom values over the representative slice.\n');
for j=1:512
    for i=1:512
        if Irep(i,j) >= Pcut
            Pabv(l) = Irep(i,j);
            l = l + 1;
        end
    end
 end
Pavg = uint16(mean(Pabv))
Pstd = uint16(std(Pabv))


fprintf('Making the replacements.\n');
for k=1:124
    slicename = strcat('CT.1.2.826.0.1.3680043.2.200.112140866.146.77330.2230.',num2str(k),'.dcm');
    I = dicomread(strcat('.\m4\',slicename));
    Imetadata = dicominfo(strcat('.\m4\',slicename));
        
    for j=1:512
        for i=1:512

        
            % Make the replacement.
            if (i>=241 & i<=247 & j>=254 & j<=261 & k>=64 & k<=76)          % Top chamber
                if (I(i,j) <= Pavg-2*Pstd || I(i,j) <= Pavg+3.25*Pstd)
                    % Do nothing
                end
            elseif (i>=269 & i<=276 & j>=253 & j<=261 & k>=63 & k<=75)      % Bottom chamber
                if (I(i,j) <= Pavg-2*Pstd || I(i,j) >= Pavg+3.25*Pstd)
                    % Do nothing
                end
            elseif (I(i,j) >= Pavg-5*Pstd)                                  % Rest of the phantom
                I(i,j) = Pavg;
            end
            
            % Fix random pixels
            if (i>1 & i<512 & j>1 & j<512)
                if (~(i>241 & i<276 & j>253 & j<261) & (i<257 || i>259))
                    A = I(i-1,j)   + I(i,j-1)   + I(i-1,j-1) + ...  % Compute sum of adjacent 8 pixels
                        I(i+1,j+1) + I(i+1,j)   + I(i,j+1)   + ...
                                     I(i-1,j+1) + I(i+1,j-1);
                    if A >= Pavg*6
                        I(i,j) = Pavg;
                    end
                end
            end
            
            %Fix slanted slices.
            if (k>=32 & k<38)
                I(i,j) = R(i,j,38);
            elseif (k>92 & k<=96)
                I(i,j) = R(i,j,92);
            end
            
            % Fix section that seems to have an unexplained dip in density.
            % Rather, just ignore the dip and manually replace.
            if (i>247 & i<257 & j>200 & j<300 & k>32 & k<96)
                    I(i,j) = Pavg;
            elseif (i>259 & i<269 & j>200 & j<300 & k>32 & k<96)
                    I(i,j) = Pavg;
            end
            
            R(i,j,k) = I(i,j);
        end
    end

    % Write the new image slice.
    dicomwrite(I, strcat('.\m4\',slicename), Imetadata);
    
    
    % Write a short progress note.
    fprintf('Finished slice %i of 124.\n', k);
    
end


fprintf('____________\n|\n| Finished\n|___________\n\n');

%
%end
%