local tool = script.Parent  -- Reference to the Tool
local slapRange = 10  -- Range within which the slap can hit

-- Function to play the slap animation and deal damage
local function playSlapAndDamage()
    local character = tool.Parent  -- The character holding the tool
    local humanoid = character:FindFirstChild("Humanoid")  -- Find the Humanoid
    if humanoid and humanoid.RigType == Enum.HumanoidRigType.R6 then  -- Ensure R6 compatibility
        local animator = humanoid:FindFirstChild("Animator")
        if not animator then
            animator = Instance.new("Animator")
            animator.Parent = humanoid
        end

        -- Play the slap animation
        local animation = Instance.new("Animation")
        animation.AnimationId = "rbxassetid://139676321685068"  -- Correct animation ID
        local animationTrack = animator:LoadAnimation(animation)
        animationTrack.Priority = Enum.AnimationPriority.Action  -- Set priority to Action
        animationTrack:Play()

        -- Detect and damage nearby players or rigs
        for _, descendant in pairs(workspace:GetDescendants()) do
            if descendant:IsA("Model") and descendant ~= character then
                local targetHumanoid = descendant:FindFirstChild("Humanoid")
                local targetPrimaryPart = descendant.PrimaryPart or descendant:FindFirstChild("HumanoidRootPart")
                local characterPrimaryPart = character.PrimaryPart or character:FindFirstChild("HumanoidRootPart")

                if targetHumanoid and targetPrimaryPart and characterPrimaryPart then
                    local distance = (characterPrimaryPart.Position - targetPrimaryPart.Position).Magnitude
                    if distance <= slapRange then  -- Check if within slap range
                        targetHumanoid:TakeDamage(10)  -- Deal 10 damage
                        print(descendant.Name .. " was slapped! Remaining HP: " .. targetHumanoid.Health)

                        -- Set the creator object
                        local player = game.Players:GetPlayerFromCharacter(character)
                        if player then
                            local creator = Instance.new("ObjectValue")
                            creator.Name = "creator"
                            creator.Value = player
                            creator.Parent = targetHumanoid
                            game.Debris:AddItem(creator, 2)  -- Remove after 2 seconds
                        end
                    end
                end
            end
        end
    else
        warn("Humanoid not found or incompatible rig type!")
    end
end

-- Connect the Tool's Activated event to play the animation and deal damage
tool.Activated:Connect(playSlapAndDamage)
