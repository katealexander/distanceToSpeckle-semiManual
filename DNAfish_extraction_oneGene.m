%% extract data to, then extract data from (directories)
%%
extractionDir = '/YOURDIRECTORYNAME';
bigDataDir = '/YOURDIRECTORYNAME';
%% extract transcription site data
clearvars -except bigDataDir extractionDir

% name of folder that experiment is actually in
folder = {...
''};
eid = {...
    '/speckle_p53targ'};
%exon then intron
eichannels = {...
    'gfp','cy'};


for i = 1:length(folder)
    cd(strcat(bigDataDir, char(folder(i))));
    objectNumber = [];
    arrayNumber = [];
    intronX = [];
    intronY = [];
    intronZ = [];
    intronIntensity = [];
    exonX = [];
    exonY = [];
    clickedX = [];
    clickedY = [];
    exonZ = [];
    exonIntensity = [];
    
    x = table(objectNumber, arrayNumber, ...
        intronX, intronY, intronZ, intronIntensity, ...
        exonX, exonY, exonZ, clickedX, clickedY, exonIntensity);
    tools = improc2.launchImageObjectTools;
    
    % while you still have stuff to look at, goes through object by object
    while tools.iterator.continueIteration
        % take only objects that have 'isGood' box checked
        if (~tools.annotations.getValue('isGood'))
            tools.iterator.goToNextObject;
            continue;
        end
        exonX = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).ExonXs;
        exonY = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).ExonYs;
        exonZ = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).ExonZs;
        clickedX = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).ClickedXs;
        clickedY = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).ClickedYs;
        
        if (isempty(exonZ))
            exonZ = zeros(1,length(exonX))';
        end
        
        if (isempty(clickedX))
            clickedX = zeros(1,length(exonX))';
        end
        
        if (isempty(clickedY))
            clickedY = zeros(1,length(exonX))';
        end
        
        if (length(exonX) < length(clickedX))
        	if (length(exonX) == 1)
        		exonX(numel(clickedX)) = 0;
        		exonX = exonX';
        	end
        	
        	exonX(numel(clickedX)) = 0;
        end
        
        if (length(exonY) < length(clickedY))
        	if (length(exonY) == 1)
        		exonY(numel(clickedY)) = 0;
        		exonY = exonY';
        	end
        	exonY(numel(clickedY)) = 0;
        end
        
        if (length(exonZ) < length(clickedY))
        	if (length(exonZ) == 1)
        		exonZ(numel(clickedY)) = 0;
        		exonZ = exonZ';
        	end
        	exonZ(numel(clickedY)) = 0;
        end
        
        exonIntensity = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).Intensity;
        exonIntensity = exonIntensity';
        
        if (length(exonIntensity) < length(clickedY))
     	   if (length(exonIntensity) == 1)
        		exonIntensity(numel(clickedY)) = 0;
        		exonIntensity = exonIntensity';
        	end
        	exonIntensity(numel(clickedY)) = 0;
        end
        
        intronX = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).IntronXs;
        intronY = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).IntronYs;
        intronZ = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).IntronZs;
        if (isempty(intronX))
            intronX = zeros(1,length(exonX))';
        end
        
        if (isempty(intronY))
            intronY = zeros(1,length(exonX))';
        end
        
        if (isempty(intronZ))
            intronZ = zeros(1,length(exonX))';
        end
        
        if (length(intronX) < length(clickedX))
        	if (length(intronX) == 1)
        		intronX(numel(clickedY)) = 0;
        		intronX = intronX';
        	end
        	intronX(numel(clickedX)) = 0;
        end
        
        if (length(intronY) < length(clickedY))
        	if (length(intronY) == 1)
        		intronY(numel(clickedY)) = 0;
        		intronY = intronY';
        	end
        	intronY(numel(clickedY)) = 0;
        end
        
        if (length(intronZ) < length(clickedY))
        	if (length(intronZ) == 1)
        		intronZ(numel(clickedY)) = 0;
        		intronZ = intronZ';
        	end
        	intronZ(numel(clickedY)) = 0;
        end
        
        intronIntensity = tools.objectHandle.getData(strcat(eichannels(i, 1), eichannels(i, 2), ':TxnSites')).IntronIntensity;
        intronIntensity = intronIntensity';
        if (isempty(intronIntensity))
            intronIntensity = zeros(1,length(exonX))';
        end
        
        if (length(intronIntensity) < length(clickedY))
        	if (length(intronIntensity) == 1)
        		intronIntensity(numel(clickedY)) = 0;
        		intronIntensity = intronIntensity';
        	end
        	intronIntensity(numel(clickedY)) = 0;
        end
       
       
        objectNumber = repmat(tools.navigator.currentObjNum(), [length(intronX) 1]);
        arrayNumber = repmat(tools.navigator.currentArrayNum(), [length(intronX) 1]);
        x = [x; table(objectNumber, arrayNumber, ...
        intronX, intronY, intronZ, intronIntensity, ...
        exonX, exonY, exonZ, clickedX, clickedY, exonIntensity)];
        tools.iterator.goToNextObject()
    end

    filename = strcat(extractionDir, char(eid(i)), '.csv');
    writetable(x, char(filename));
end