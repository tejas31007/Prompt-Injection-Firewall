from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from firewall import AIFirewall
from database import DatabaseLogger

# Initialize the API app
app = FastAPI(
    title="Prompt Injection Firewall",
    description="An AI security gateway that scores and filters malicious prompts.",
    version="1.0.0"
)

# Initialize our firewall engine and database logger
print("Starting up the firewall engine...")
firewall_engine = AIFirewall()

print("Connecting to the database...")
db_logger = DatabaseLogger()

# Define the expected JSON payload structure
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    """Simple health check endpoint."""
    return {"status": "Active", "message": "Firewall API is running securely."}

@app.post("/api/v1/scan")
def scan_input(request: PromptRequest):
    """
    Receives a prompt from the user, passes it through the firewall,
    and automatically logs it to the database if it is malicious.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
        
    # Send the text to the firewall
    verdict = firewall_engine.scan_prompt(request.prompt)
    
    # --- NEW LOGIC: Save to database if blocked ---
    if verdict["status"] == "BLOCKED":
        db_logger.log_attack(
            prompt=request.prompt,
            layer_failed=verdict["reason"],
            threat_score=verdict["score"]
        )
    
    return verdict