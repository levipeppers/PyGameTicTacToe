local tool = script.Parent

-- RemoteEvent to communicate with the client
local remoteEvent = Instance.new("RemoteEvent")
remoteEvent.Name = "PlaySlapAnimation"
remoteEvent.Parent = tool

-- Function to trigger the animation on the client
tool.Activated:Connect(function()
    local character = tool.Parent  -- The character holding the tool
    local player = game.Players:GetPlayerFromCharacter(character)
    if player then
        remoteEvent:FireClient(player)  -- Notify the client to play the animation
    end
end)
