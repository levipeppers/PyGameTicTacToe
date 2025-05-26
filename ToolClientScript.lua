local tool = script.Parent
local remoteEvent = tool:WaitForChild("PlaySlapAnimation")

-- Function to play the slap animation
local function playSlapAnimation()
    local character = tool.Parent  -- The character holding the tool
    local humanoid = character:FindFirstChild("Humanoid")
    if humanoid then
        local animator = humanoid:FindFirstChild("Animator") or Instance.new("Animator", humanoid)
        local animation = Instance.new("Animation")
        animation.AnimationId = "rbxassetid://139676321685068"  -- Correct animation ID

        local animationTrack = animator:LoadAnimation(animation)
        animationTrack.Priority = Enum.AnimationPriority.Action  -- Set priority to Action
        animationTrack:Play()  -- Play the animation
    end
end

-- Listen for the RemoteEvent to play the animation
remoteEvent.OnClientEvent:Connect(playSlapAnimation)
