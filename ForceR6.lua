game.Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function(character)
        local humanoid = character:WaitForChild("Humanoid")
        if humanoid then
            if humanoid.RigType ~= Enum.HumanoidRigType.R6 then
                humanoid.RigType = Enum.HumanoidRigType.R6  -- Force R6 rig type
                print(player.Name .. " has been switched to R6.")
            end
        else
            warn("Humanoid not found for " .. player.Name)
        end
    end)
end)
