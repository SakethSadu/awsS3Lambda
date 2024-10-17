from getSftpCreds import get_secret
import boto3;
import paramiko;
from paramiko import SFTPClient;

s3_client = boto3.client('s3')
#function to upload file like object to S3
def uploadToS3 (fileObj, s3BucketName, s3FileKey):
    try:
        s3_client.upload_fileobj (fileObj, s3BucketName, s3FileKey)
        print(f"Uploaded to s3 ://{s3BucketName}/{s3FileKey}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

#function to handle only one file:

def transferFileSFTPToS3(sftp, remoteDirectory, remoteFileName, s3BucketName, s3FileKey):
    try:
        # Construct the full remote file path
        remoteFilePath = f"{remoteDirectory}/{remoteFileName}"
        
        # Check if the specific file exists in the remote directory
        if remoteFileName in sftp.listdir(remoteDirectory):
            with sftp.file(remoteFilePath, 'rb') as fileObj:
                print(f"Transferring {remoteFileName} from SFTP to S3....")
                uploadToS3(fileObj, s3BucketName, s3FileKey)
        else:
            print(f"File {remoteFileName} not found in the remote directory.")
            
    except Exception as e:
        print(f"Error during Transfer from SFTP to S3: {e}")


#function to Transfer files from SFTP server to S3 Bucket

def transferSFTPToS3(sftp, remoteDirectory, s3BucketName):
    try:
        fileList = sftp.listdir(remoteDirectory)
        for file in fileList:
            remoteFilePath = f"{remoteDirectory}/{file}"

            with sftp.file(remoteFilePath, 'rb') as fileObj:
                print(f"Transferring {file} from SFTP to S3....")
                uploadToS3(fileObj, s3BucketName, file)
    except Exception as e:
        print(f"Error during Transfer from SFTP to S3: {e}")




# Main function to run the code
# def main():

#     #our secret key name in AWS Secret Manager.
#     secret_name = "sftp_details";   
#     credentials = get_secret(secret_name)

#     if credentials:
#         #your Bucket name where you want to store the files
#         s3BucketName = "my-s3-bucket-sakethtest3"

#         transport = paramiko.Transport(credentials['sftp_host'], int(credentials['sftp_port']))

#         try:
#             transport.connect(username=credentials['sftp_username'], password=credentials['sftp_password'])
#             sftp = SFTPClient.from_transport(transport)

#             #the folder and files detials which ywe want to transfer from sftp to s3
#             remoteDirectory = "C:/Users/sakethssh"
#             remoteFileName = "test12.csv"
#             s3FileKey = "File1Today.csv"

#             transferFileSFTPToS3(sftp,remoteDirectory, remoteFileName, s3BucketName,s3FileKey)
#             #transferSFTPToS3(sftp, remoteDirectory, s3BucketName)

#         except Exception as e:
#             print(f"Error connecting to SFTP : {e}")

#         finally:
#             sftp.close()
#             transport.close()


# if __name__ == "__main__":
#     main()