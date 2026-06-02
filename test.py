"""
Test Folder Access
"""

from utils.google_drive import get_drive_service, GOOGLE_DRIVE_FOLDERS

print("="*70)
print("🔍 TESTING FOLDER ACCESS")
print("="*70)

service = get_drive_service()

if not service:
    print("\n❌ Authentication failed!")
    exit(1)

print("\n✅ Service connected")

print("\n📁 Testing folder access:")
print("-"*70)

for entity_type, folder_id in GOOGLE_DRIVE_FOLDERS.items():
    print(f"\n{entity_type}:")
    print(f"  Folder ID: {folder_id}")
    
    try:
        folder = service.files().get(
            fileId=folder_id,
            fields='id, name, owners, permissions'
        ).execute()
        
        print(f"  ✅ Name: {folder.get('name')}")
        print(f"  Owner: {folder.get('owners', [{}])[0].get('emailAddress', 'Unknown')}")
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        
        if "404" in str(e):
            print(f"  → Folder not found with this ID")
        elif "403" in str(e):
            print(f"  → No permission to access this folder")

print("\n" + "="*70)