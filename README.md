This tool uses webdriver to automatically take screenshots of PufferPanel 3.x  
It was built to make it easier to update the PufferPanel documentation with up to date screenshots, but it might also prove useful to create screenshots to show off your custom themes
To cover everything it goes through all pages twice, once with the browser set to prefer light mode, once with it preferring dark mode

## Dependencies

This tool expects [geckodriver](https://github.com/mozilla/geckodriver) to be installed and available from `$PATH`  
Once geckodriver is installed run `pip install -r requirements.txt` to make the needed python packages available locally

## Usage

Run the `screens.py` script with any of the following flags

| Flag               | Description                                                                                                                                                            | Default                  | Required |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|----------|
| `-U`, `--url`      | The URL of the running PufferPanel instance to take screenshots of                                                                                                     | `http://localhost:8080/` | No       |
| `-e`, `--email`    | The email to log into the panel with                                                                                                                                   | None                     | Yes      |
| `-s`, `--server`   | The ID of the server to take screenshots of, doesn't take screenshots of the server view if no ID is given                                                             | None                     | No       |
| `-n`, `--node`     | The ID of the node to take screenshots of, doesn't take screenshots of the node view if no ID is given                                                                 | None                     | No       |
| `-u`, `--user`     | The ID of the user to take screenshots of, doesn't take screenshots of the user view if no ID is given                                                                 | None                     | No       |
| `-t`, `--template` | The ID of the template to take screenshots of, doesn't take screenshots of the template view if no ID is given                                                         | None                     | No       |
| `-o`, `--output`   | Where the screenshots are saved to                                                                                                                                     | `out`                    | No       |
| `-H`, `--head`     | When this flag is given it will show the automated browser window                                                                                                      |                          | No       |
| `-d`, `--delay`    | How long to wait after loading a page to let everything else load                                                                                                      | `0.75`                   | No       |
| `-x`, `--width`    | The width of the browser window, indirectly determines screenshot width                                                                                                | `1920`                   | No       |
| `-y`, `--height`   | The height of the browser window, indirectly determines screenshot height<br>Screenshots aren't exactly this height due to the address bar taking up some of the space | `1080`                   | No       |

Example: `./screens.py -e email@example.com --server 724673c0`

The script will ask for the password to the given account so it can create screenshots of the logged in areas

Once started it will print information on what it's doing to the terminal, the process may take a while

Make sure the given account has its theme preferences set to the theme you want to take screenshots of and to use light or dark mode based on browser preferences if the theme supports it so you get both in one go
