local kills = Instance.new("IntValue")
kills.Name = "Kills"
kills.Value = 0
kills.Parent = leaderstats

playerVariables[player.UserId] = kills
print("Leaderboard initialized for player:", player.Name)

-- Hook character spawning
player.CharacterAdded:Connect(function(character)
    local humanoid = character:WaitForChild("Humanoid")

    humanoid.Died:Connect(function()
        local creator = humanoid:FindFirstChild("creator")
        if creator and creator.Value and creator.Value:IsA("Player") then
            local killer = creator.Value
            local killerStats = killer:FindFirstChild("leaderstats")
            if killerStats then
                local killerKills = killerStats:FindFirstChild("Kills")
                if killerKills then
                    killerKills.Value += 1
                    print(killer.Name .. " now has " .. killerKills.Value .. " kills!")
                end
            end
        else
            print("No valid killer found for", player.Name)
        end
    end)
end)

-- Only connect input listener ONCE per player on client (for local scripts)
-- But since you're doing this server-side, we need to move it to a **LocalScript** to avoid bugs.