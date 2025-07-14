#!/usr/bin/env python3
"""
Test script to verify MCP server integration with Cursor AI
"""

import requests
import json

# Your MCP server URL
MCP_SERVER_URL = "https://psq-nwrf.onrender.com"

def test_api_endpoints():
    """Test the FastAPI endpoints"""
    print("Testing FastAPI endpoints...")
    
    # Test list_databases
    try:
        response = requests.get(f"{MCP_SERVER_URL}/list_databases")
        print(f"✅ list_databases: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ list_databases failed: {e}")
    
    # Test list_tables
    try:
        response = requests.get(f"{MCP_SERVER_URL}/list_tables")
        print(f"✅ list_tables: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ list_tables failed: {e}")
    
    # Test get_relationships
    try:
        response = requests.get(f"{MCP_SERVER_URL}/get_relationships")
        print(f"✅ get_relationships: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ get_relationships failed: {e}")

def test_cursor_config():
    """Test the Cursor configuration"""
    print("\nTesting Cursor configuration...")
    
    try:
        with open('.cursorrules', 'r') as f:
            config = json.load(f)
        
        if 'mcpServers' in config and 'postgres-mcp' in config['mcpServers']:
            server_config = config['mcpServers']['postgres-mcp']
            if 'url' in server_config and server_config['url'] == MCP_SERVER_URL:
                print("✅ .cursorrules configuration is correct")
            else:
                print("❌ .cursorrules configuration is incorrect")
        else:
            print("❌ .cursorrules missing MCP server configuration")
    except Exception as e:
        print(f"❌ Error reading .cursorrules: {e}")

def main():
    print("🧪 Testing PostgreSQL MCP Server Integration")
    print("=" * 50)
    
    test_api_endpoints()
    test_cursor_config()
    
    print("\n" + "=" * 50)
    print("🎉 Integration test complete!")
    print("\nTo use in Cursor AI:")
    print("1. Make sure .cursorrules is in your project root")
    print("2. Restart Cursor if needed")
    print("3. Try asking: 'List all databases' or 'Show me the tables'")

if __name__ == "__main__":
    main() 