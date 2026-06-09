-- LLM Diplomat Script for VCMI
-- HTTP request to FastAPI server running HoMM3 LLM Diplomacy API

local http = require("socket.http")
local ltn12 = require("ltn12")
local json = require("json")

-- Configuration
local API_URL = "http://localhost:8000/chat"
local API_TIMEOUT = 5

print("[LLM Diplomat] Script loaded successfully!")

-- Helper function to make HTTP POST request to FastAPI
local function call_llm_api(game_context)
    print("[LLM Diplomat] Sending request to " .. API_URL)
    
    local json_data = json.encode(game_context)
    print("[LLM Diplomat] Payload size: " .. #json_data .. " bytes")
    
    local response_body = {}
    local request_headers = {
        ["Content-Type"] = "application/json",
        ["Content-Length"] = tostring(#json_data)
    }
    
    local res, code, response_headers = http.request {
        url = API_URL,
        method = "POST",
        headers = request_headers,
        source = ltn12.source.string(json_data),
        sink = ltn12.sink.table(response_body)
    }
    
    if code == 200 then
        local response = table.concat(response_body)
        print("[LLM Diplomat] Response received (length: " .. #response .. ")")
        local decoded = json.decode(response)
        return decoded
    else
        print("[LLM Diplomat] Error: HTTP " .. tostring(code))
        return nil
    end
end

-- Create game context matching app.py GameContext schema
local function create_sample_context()
    return {
        time = {
            month = 1,
            week = 1,
            day = 1
        },
        bot_resources = {
            gold = 5000,
            wood = 50,
            ore = 40,
            mercury = 20,
            sulfur = 15,
            crystal = 10,
            gems = 5
        },
        player_resources = {
            gold = 3000,
            wood = 30,
            ore = 20,
            mercury = 10,
            sulfur = 5,
            crystal = 5,
            gems = 2
        },
        bot_army_value = 500,
        player_army_value = 250,
        bot_hero = {
            name = "Красний лицар",
            hero_class = "knight",
            attack = 12,
            defense = 10,
            spell_power = 2,
            knowledge = 3,
            current_mana = 10,
            army = {
                { name = "Піхотинець", count = 50 },
                { name = "Лучник", count = 30 },
                { name = "Гриф", count = 10 }
            }
        },
        player_hero = {
            name = "Гравець",
            hero_class = "ranger",
            attack = 10,
            defense = 9,
            spell_power = 3,
            knowledge = 4,
            current_mana = 20,
            army = {
                { name = "Піхотинець", count = 30 }
            }
        },
        map_info = {
            distance_to_player = 5,
            terrain = "plain",
            distance_to_bot_castle = 10
        },
        player_message = "Пропоную мир за 2000 золота",
        bot_personality = "Ти агресивний та прямолінійний. Вважаєш силу головним аргументом. Любиш атакувати першим."
    }
end

-- Process AI response (app.py returns ModelResponse with dialogue_text and actions)
local function process_response(response)
    if not response then
        print("[LLM Diplomat] No response received")
        return
    end
    
    print("\n[LLM Diplomat] ===== AI RESPONSE =====")
    print("Bot says: " .. (response.dialogue_text or "..."))
    print("Actions count: " .. #(response.actions or {}))
    
    if response.actions and #response.actions > 0 then
        for i, action in ipairs(response.actions) do
            print("\nAction " .. i .. ":")
            print("  Type: " .. action.type)
            print("  Params: " .. json.encode(action.params))
            
            -- Here you would implement actual game actions:
            -- if action.type == "attack" then
            --     -- execute attack logic
            -- elseif action.type == "retreat" then
            --     -- execute retreat logic
            -- elseif action.type == "transfer_resources" then
            --     -- transfer resources between players
            -- elseif action.type == "set_alliance" then
            --     -- create alliance between players
            -- end
        end
    end
    print("[LLM Diplomat] =======================\n")
end

-- Main test function
function test_llm_diplomat()
    print("\n[LLM Diplomat] ===== STARTING TEST =====")
    print("[LLM Diplomat] Creating sample game context...")
    
    local context = create_sample_context()
    
    print("[LLM Diplomat] Calling FastAPI at " .. API_URL)
    local response = call_llm_api(context)
    
    if response then
        process_response(response)
        print("[LLM Diplomat] Test completed successfully!")
    else
        print("[LLM Diplomat] Test failed - no response from API")
        print("[LLM Diplomat] Make sure FastAPI server is running on " .. API_URL)
    end
end

-- Register console command
if game and game.registerCommand then
    game.registerCommand("llm_test", function()
        test_llm_diplomat()
    end)
    print("[LLM Diplomat] Command registered: /llm_test")
end

print("[LLM Diplomat] Ready! Use '/llm_test' command to test")
