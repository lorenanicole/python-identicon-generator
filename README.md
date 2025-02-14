# Python Identicon Generator

A Python 3.10 CLI script that generates identicons. Default size for identicons created is 320X320 pixels, as this is the recommended size by many social media platforms like Instagram.

For help running the script use `python3 main.py -h` to retrieve a usage prompt and overview of parameters including optional parameters.

Usage:
1. Only providing the input `-t` text: `python3 main.py -t helloworld`. 
2. Providing the input `-t` text and a specified output `-o` name for the ouput `*.png` identicon: `python3 main.py -t helloworld -o helloworld`. 
3. Providing the input `-t` text and a specified output `-o` name for the ouput `*.png` identicon and overriding default dimensions of 320X320 pixels e.g. 150X150 pixels: `python3 main.py -t helloworld -o helloworld -d 150`. 

**Using Codespaces**

*To start:*
- From the private repo page, select <> Code button <> Codespaces
- Spin up a new Codespace!
- Select option that says, "open in browser" and you won't need to bootstrap anything! Thw `.devcontainer` is configured to handle the dependencies installation.

*To stop:*
But please remember upon completing with Codespaces to turn it down (as there's only so many billable hours permitted per account). 
- This can be done by closing the browser tab with the Codespace and returning to the private repo
- Click <> Code, click next to "fantastic barnacle" via the three ellipses
- Select "stop Codespace"

## Requirements
1. The identicon's should be symmetrical meaning the left horizontal half is equal to the right horizontal half.
2. The identicon is 5X5 pixels, following the standard specified for [GitHub identicons](https://github.blog/2013-08-14-identicons/), so we'll generate square identicons only with a default of 320X320 pixels which other social media platforms like Instagram define as an ideal size
3. Identicon's should use proper resizing sampling technique to ensure quality is maintained, see [Pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize) documentation for options
4. Avoid replicating creating identicon by confirming if an image for said user has been generated, if so retrieve from a persistence layer. A NoSQL solution like mongodb would be useful, but we'll use a modified version of `@lru_cache` from the `sweepai` project - `@file_cache` which persists pickled objects between runs.

## Questions

Contact me, [Lorena Mesa](http://lorenamesa.com)!
