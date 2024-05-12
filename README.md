# User session count

### Version used: Python3.11
### Additional Libraries: Pandas==2.2.2
### OS on which tested: MacOS Ventura

### Explnation of code execution:
- Code accepts the file path as the simple input, if given file path does not exist then it is handled by an exception
- There are two function:
  > 1. calc_session_time:
  >    This function accepts the file path and read the txt file using Pandas Dataframe
  >    First of all timestamp calculatipon has been perfromed for session where Start and End session is available
  >    Later separate calculation has been performed for the session where only Start or only End marker is available
  >    Session related information has been stored in hash map which has been dynamically generated based on user list
  >    This function returns has map which contains user and their session count, timestamp calculation related infromation
  > 3. print_record
  >    This function accepts user list and hash map which contains data related with user, their timestamp and sesion count and print it in desired format
