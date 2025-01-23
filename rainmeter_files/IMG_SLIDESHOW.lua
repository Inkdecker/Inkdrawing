function Initialize()
    file_path = SKIN:GetVariable('ImagePreset')
    closeThreshold = tonumber(SKIN:GetVariable('CloseThreshold')) or 1
    imgTable = {}
    for line in io.lines(SKIN:MakePathAbsolute(file_path)) do
        table.insert(imgTable, line)
    end

    -- Create a list of indices
    indexList = {}
    for i = 1, #imgTable do
        table.insert(indexList, i)
    end

    -- Shuffle the list of indices
    math.randomseed(os.time())
    for i = #indexList, 2, -1 do
        local j = math.random(i)
        indexList[i], indexList[j] = indexList[j], indexList[i]
    end

    currentIndex = 1
    currentQuoteIndex = indexList[currentIndex]

end


-- Global variable to track the last time CopyFilePath was called
lastCopyTime = 0

function CopyFilePath()
    -- Get the current file path
    local filePath = imgTable[currentQuoteIndex]

    -- Copy the file path to the clipboard
    SKIN:Bang('!SetClip', filePath)

    -- Update the last copy time
    lastCopyTime = os.clock()


end

function CloseSlideshow()
    -- Get the current time
    local currentTime = os.clock()

    -- Check if at least 1 second has passed since CopyFilePath was called
    if currentTime - lastCopyTime >= closeThreshold then
        -- Close the slideshow
        SKIN:Bang('!DeactivateConfig')
    else
        -- Log a message or notify the user that closing is not allowed yet
        SKIN:Bang('!Log', 'Cannot close the slideshow: CopyFilePath was used less than ' .. closeThreshold .. ' seconds ago.', 'Warning')
    end
end




function Update()
    currentIndex = currentIndex + 1
    if currentIndex > #imgTable then
        currentIndex = 1
    end
    currentQuoteIndex = indexList[currentIndex]
    SKIN:Bang('!Log', currentIndex..' - '..tostring(currentQuoteIndex)..'  update', 'Debug')
    return imgTable[currentQuoteIndex]
end

function PreviousQuote()
    currentIndex = currentIndex - 2
    if currentIndex < 0 then
        currentIndex = #imgTable - 1
    end
    currentQuoteIndex = indexList[currentIndex]
    
    return imgTable[currentQuoteIndex]
end

function NextQuote()
    if currentIndex > #imgTable then
        currentIndex = 1
    end
    currentQuoteIndex = indexList[currentIndex]
    
    return imgTable[currentQuoteIndex]
end




function Delete_File()

    local filePath = imgTable[currentQuoteIndex]  
    -- Define the destination folder path
    local tmpFolderPath = SKIN:GetVariable('DeletedFilesFolder') 
    -- Construct the move command
    local filename = filePath:match("^.+\\([^\\]+)$")
    local new_filePath = tmpFolderPath .. filename

    -- Rename the file to swap folders
    local success, err = os.rename(filePath, new_filePath)


    -- Remove the entry from imgTable

    table.remove(imgTable, currentQuoteIndex)

    -- Update the text file with the modified content
    local file = io.open(SKIN:MakePathAbsolute(file_path), "w")
    if not file then
        print("Error: Unable to open file for writing.")
        return
    end

    -- Write the modified content to the file
    for _, line in ipairs(imgTable) do
        file:write(line .. "\n")
    end
    -- Close the file
    file:close()
end


function OpenFolder()
    local filePath = imgTable[currentQuoteIndex]
    
    -- Use explorer command to open the folder and select the current image
    os.execute('explorer /select,"' .. filePath .. '"')
end
