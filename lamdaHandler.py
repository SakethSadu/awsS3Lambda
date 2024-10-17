
import paramiko;
from paramiko import SFTPClient;
from getSftpCreds import get_secret
from s3FileTransfer import uploadToS3, transferFileSFTPToS3, transferSFTPToS3

def lambda_handler(event, context):
    secret_name = "sftp_details";   
    credentials = get_secret(secret_name)

    if credentials:
        #your Bucket name where you want to store the files
        s3BucketName = "my-s3-bucket-sakethtest3"

        transport = paramiko.Transport(credentials['sftp_host'], int(credentials['sftp_port']))

        try:
            transport.connect(username=credentials['sftp_username'], password=credentials['sftp_password'])
            sftp = SFTPClient.from_transport(transport)

            #the folder and files detials which ywe want to transfer from sftp to s3
            remoteDirectory = "C:/Users/sakethssh"
            remoteFileName = "test12.csv"
            s3FileKey = "File1Today.csv"

            transferFileSFTPToS3(sftp,remoteDirectory, remoteFileName, s3BucketName,s3FileKey)
            #transferSFTPToS3(sftp, remoteDirectory, s3BucketName)

        except Exception as e:
            print(f"Error connecting to SFTP : {e}")

        finally:
            sftp.close()
            transport.close()