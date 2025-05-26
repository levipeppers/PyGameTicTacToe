game.Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function(character)
        local humanoid = character:WaitForChild("Humanoid")
        if humanoid then
            -- Force R6 rig type
            humanoid.RigType = Enum.HumanoidRigType.R6
            print(player.Name .. " has been switched to R6.")

            -- Replace default animations with R6 animations
            local animateScript = character:FindFirstChild("Animate")
            if animateScript then
                animateScript:Destroy()  -- Remove the default animation script
            end

            -- Add R6 animations
            local newAnimateScript = Instance.new("LocalScript", character)
            newAnimateScript.Name = "Animate"
            newAnimateScript.Source = [[
                local animate = script.Parent
                local humanoid = animate.Parent:WaitForChild("Humanoid")

                -- R6 Animation IDs
                local animations = {
                    walk = "rbxassetid://180426354",  -- R6 walk animation
                    jump = "rbxassetid://125750702",  -- R6 jump animation
                    climb = "rbxassetid://180436334", -- R6 climb animation
                    fall = "rbxassetid://180436148",  -- R6 fall animation
                    idle = "rbxassetid://180435571",  -- R6 idle animation
                }

                -- Function to load animations
                local function loadAnimation(animationId)
                    local animation = Instance.new("Animation")
                    animation.AnimationId = animationId
                    return humanoid:LoadAnimation(animation)
                end

                -- Play animations
                humanoid.Running:Connect(function(speed)
                    if speed > 0 then
                        loadAnimation(animations.walk):Play()
                    end
                end)

                humanoid.Jumping:Connect(function()
                    loadAnimation(animations.jump):Play()
                end)

                humanoid.Climbing:Connect(function()
                    loadAnimation(animations.climb):Play()
                end)

                humanoid.FreeFalling:Connect(function()
                    loadAnimation(animations.fall):Play()
                end)

                humanoid.StateChanged:Connect(function(_, newState)
                    if newState == Enum.HumanoidStateType.Idle then
                        loadAnimation(animations.idle):Play()
                    end
                end)
            ]]
        end
    end)
end)
