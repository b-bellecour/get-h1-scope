Sure! Below is the complete `README.md` file with all the text included in Markdown format:

### README.md


# Get HackerOne Scope

This script fetches and organizes scope information from HackerOne public and enrolled private programs.

## Description

The `get-h1-scope.py` script helps you fetch scope URLs from HackerOne programs and save them in an organized manner. You can use it to fetch scopes from both public programs (by specifying the program handle) and private programs you are enrolled in.

- thanks to @sw33tLie for the cool bbscope tool!

## Usage

### Fetching Private Program Scope

To fetch the scope for private programs you are enrolled in:

```
./get-h1-scope.py -p
```

The output will be saved under:
```
/home/<system_username>/bugBounty/private-bugbounty/<scope_name>/<scope_name>-scope.txt
```

### Fetching Public Program Scope

To fetch the scope for a public program, provide the program handle as an argument:

```
./get-h1-scope.py netflix
```

The output will be saved under:
```
/home/<system_username>/bugBounty/<program_handle>/<program_handle>-scope.txt
```

When using a program handle, the input should be the program name as it appears in the URL, e.g., `netflix` for `https://hackerone.com/netflix/policy_scopes`.

### Example Usage

```
./get-h1-scope.py -p
(Fetch the private program scope you are enrolled in)

./get-h1-scope.py netflix
(Fetch the scope for the "netflix" program)
```

## Installation

1. **Clone the repository:**

    ```
    git clone https://github.com/<your-username>/<your-repository>.git
    cd <your-repository>
    ```

2. **Ensure you have the required dependencies:**

    - Python 3.x
    - `requests` library (Install using `pip install requests`)

3. **Set up your environment variables:**

    Add the following lines to your `.bashrc` or `.bash_profile`:

    ```
    export H1_API_USERNAME="<your_hackerone_username>"
    export H1_API_TOKEN="<your_hackerone_api_token>"
    ```

    Apply the changes:

    ```
    source ~/.bashrc
    ```

4. **Install `bbscope` dependency:**

    - Make sure you have `go` installed. If not, install it from [here](https://golang.org/dl/).

    - Install `bbscope`:

    ```
    GO111MODULE=on go install -v github.com/sw33tLie/bbscope@latest
    ```

    - Ensure `bbscope` is in your PATH. Add the following to your `.bashrc` or `.bash_profile`:

    ```
    export PATH=$PATH:$(go env GOPATH)/bin
    ```

    Apply the changes:

    ```
    source ~/.bashrc
    ```

## License

This project is licensed under the MIT License.

## Author

Baptiste Bellecour.

