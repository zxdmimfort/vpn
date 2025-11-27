"""Example script for testing VPN service API."""

import asyncio

import httpx

BASE_URL = "http://localhost:8000"
API_KEY = "your_secret_api_key"  # Change this to your actual API key


async def main() -> None:
    """Run examples."""
    async with httpx.AsyncClient() as client:
        headers = {"X-API-Key": API_KEY}

        # Health check
        print("🏥 Checking service health...")
        response = await client.get(f"{BASE_URL}/health")
        print(f"Health: {response.json()}\n")

        # List inbounds
        print("📋 Listing inbounds...")
        response = await client.get(f"{BASE_URL}/api/v1/inbounds", headers=headers)
        if response.status_code == 200:
            inbounds = response.json()
            print(f"Found {len(inbounds)} inbounds")
            for inbound in inbounds:
                print(f"  - {inbound['remark']} (Port: {inbound['port']})")
        print()

        # Get server stats
        print("📊 Getting server statistics...")
        response = await client.get(f"{BASE_URL}/api/v1/stats/server", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"CPU Usage: {stats['cpu_usage']}%")
            print(f"Memory Usage: {stats['memory_usage']}%")
            print(f"Disk Usage: {stats['disk_usage']}%")
        print()

        # Get traffic stats
        print("📈 Getting traffic statistics...")
        response = await client.get(f"{BASE_URL}/api/v1/stats/traffic", headers=headers)
        if response.status_code == 200:
            traffic = response.json()
            for item in traffic:
                total_gb = item["total"] / (1024**3)
                print(f"Inbound {item['inbound_id']}: {total_gb:.2f} GB")


if __name__ == "__main__":
    asyncio.run(main())
