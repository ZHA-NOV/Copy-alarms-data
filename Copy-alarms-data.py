import asyncio
import aiofiles
import paramiko
import os

async def download_smb_files(server_ip, smb_share, username, password, local_destination):
    # Establish an SSH connection to the server
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(server_ip, username=username, password=password)

    # Open an SFTP session using the SSH connection
    sftp_client = ssh_client.open_sftp()

    try:
        # Change to the SMB share directory
        sftp_client.chdir(smb_share)

        # Retrieve a list of files in the SMB share
        smb_files = sftp_client.listdir()

        for smb_file in smb_files:
            smb_file_path = f"{smb_share}/{smb_file}"
            local_file_path = f"{local_destination}/{smb_file}"

            # Download the file from the SMB share to the local destination
            async with aiofiles.open(local_file_path, 'wb') as local_file:
                remote_file = sftp_client.open(smb_file_path, 'rb')
                async for chunk in remote_file.iter_chunked(1024):
                    await local_file.write(chunk)

                remote_file.close()

            print(f"Downloaded file: {smb_file}")

    except IOError as e:
        print(f"Error downloading SMB files: {e}")

    # Close the SFTP client and the SSH connection
    sftp_client.close()
    ssh_client.close()


async def execute_smb_download():
    while True:
        # Define the SMB server and authentication details
        server_ip = '10.10.10.72'  # IP address of the server
        smb_share = '/log'  # SMB share name
        username = 'CCP'  # SMB username
        password = 'Vdl@0184'  # SMB password
        local_destination = '/home/moxa/logs'  # Local destination directory

        # Create the local destination directory if it doesn't exist
        if not os.path.exists(local_destination):
            os.makedirs(local_destination)

        # Run the SMB file download coroutine
        await download_smb_files(server_ip, smb_share, username, password, local_destination)

        # Wait for 30 seconds before executing the download again
        await asyncio.sleep(30)


# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Schedule the SMB file download coroutine to run every 30 seconds [need to come up with a proper time gap]
loop.create_task(execute_smb_download())

try:
    # Run the event loop
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the event loop
loop.close()
