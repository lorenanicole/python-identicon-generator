# Python Identicon Generator

A Python 3.10 CLI script that generates identicons. Default size for identicons created is 320X320 pixels, as this is the recommended size by many social media platforms like Instagram.

For help running the script use `python3 main.py -h` to retrieve a usage prompt and overview of parameters including optional parameters.

Usage:
1. Only providing the input `-t` text: `python3 main.py -t helloworld`. 
2. Providing the input `-t` text and a specified output `-o` name for the ouput `*.png` identicon: `python3 main.py -t helloworld -o helloworld`. 
3. Providing the input `-t` text and a specified output `-o` name for the ouput `*.png` identicon and overriding default dimensions of 320X320 pixels e.g. 150X150 pixels: `python3 main.py -t helloworld -o helloworld -d 150`. 

**Using Codespaces**

*To start:*
- From the private repo page, select <> Code button
- Click the three ellipses next to the "fantastic barnacle" Codespace
- Select option that says, "open in browser" and you won't need to bootstrap anything! 

*To stop:*
But please remember upon completing with Codespaces to turn it down (as there's only so many billable hours permitted per account). 
- This can be done by closing the browser tab with the Codespace and returning to the private repo
- Click <> Code, click next to "fantastic barnacle" via the three ellipses
- Select "stop Codespace"

## Problem Prompt

Users often work collaboratively in digital environments where a profile picture is not available. Some platforms have attempted to solve this problem with the creation of randomly generated, unique icons for each user ([github](https://github.blog/2013-08-14-identicons/), [slack](https://slack.zendesk.com/hc/article_attachments/360048182573/Screen_Shot_2019-10-01_at_5.08.29_PM.png), [ethereum wallets](https://github.com/ethereum/blockies)) sometimes called *Identicons*. Given an arbitrary string, create an image that can serve as a unique identifier for a user of a B2B productivity app like slack, notion, etc.

**Example Requirements**

1. Define a set of objectives to accomplish with your identicon. There's no right or wrong answer here. Here are some hypothetical objectives:
- Legibility at some scale or set of scales 
- what sizes should the icon be shown at?
- Appearance - how do we avoid generating images that look bad?
2. Given an arbitrary string, generate an image (as a jpg, gif, png, or in a web page using canvas, webgl, or whatever other display strategy you prefer)
3. Images should be reasonably unique, for instance the strings "John", "Jane", and "931D387731bBbC988B31220" should generate three distinct images
4. Any languages may be used, any libraries may be used, recommend javascript or python
5. Don’t use an existing library! Treat this exercise as if you looked at existing solutions and thought you could do better, and decided to write your own

## Identicon Requirements (Defined)
1. The identicon's should be symmetrical meaning the left horizontal half is equal to the right horizontal half.
2. The identicon is 5X5 pixels, following the standard specified for [GitHub identicons](https://github.blog/2013-08-14-identicons/), so we'll generate square identicons only with a default of 320X320 pixels which other social media platforms like Instagram define as an ideal size
3. Identicon's should use proper resizing sampling technique to ensure quality is maintained, see [Pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize) documentation for options
4. Avoid replicating creating identicon by confirming if an image for said user has been generated, if so retrieve from a persistence layer. A NoSQL solution like mongodb would be useful, but we'll use a modified version of `@lru_cache` from the `sweepai` project - `@file_cache` which persists pickled objects between runs.

## TODO:
- [X] Implement core logic to generate a Python PIL image
- [X] Write baseline tests
- [X] Add CI/CD with GitHub actions to run tests 
- [X] Add CI/CD with GitHub Actions to run linter
