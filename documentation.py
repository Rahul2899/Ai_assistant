from datetime import datetime
import os
import json

def document_incident(incident_summary, resolution_steps, status):
    try:
        documentation = f"""
        # Incident Report

        ## Incident Summary
        {incident_summary}

        ## Resolution Status
        {status.capitalize()}

        ## Resolution Steps
        {resolution_steps}

        ## Timestamp
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        os.makedirs('reports', exist_ok=True)
        filename = f"reports/{status}_incident_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(filename, "w") as file:
            file.write(documentation)
        
        # Here you would add code to export to a database
        # For example:
        # save_to_database(status, incident_summary, resolution_steps)

        return f"Incident documented successfully. File saved as {filename}"
    except Exception as e:
        return f"An error occurred while documenting the incident: {str(e)}"