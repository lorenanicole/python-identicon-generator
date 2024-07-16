# Python Identicon Generator

## Problem Prompt

Users often work collaboratively in digital environments where a profile picture is not available. Some platforms have attempted to solve this problem with the creation of randomly generated, unique icons for each user ([github](https://github.blog/2013-08-14-identicons/), [slack](https://slack.zendesk.com/hc/article_attachments/360048182573/Screen_Shot_2019-10-01_at_5.08.29_PM.png), [ethereum wallets](https://github.com/ethereum/blockies)) sometimes called *Identicons*. Given an arbitrary string, create an image that can serve as a unique identifier for a user of a B2B productivity app like slack, notion, etc.

**Requirements**

1. Define a set of objectives to accomplish with your identicon. There's no right or wrong answer here. Here are some hypothetical objectives:
- Legibility at some scale or set of scales 
- what sizes should the icon be shown at?
- Appearance - how do we avoid generating images that look bad?
2. Given an arbitrary string, generate an image (as a jpg, gif, png, or in a web page using canvas, webgl, or whatever other display strategy you prefer)
3. Images should be reasonably unique, for instance the strings "John", "Jane", and "931D387731bBbC988B31220" should generate three distinct images
4. Any languages may be used, any libraries may be used, recommend javascript or python
5. Don’t use an existing library! Treat this exercise as if you looked at existing solutions and thought you could do better, and decided to write your own

## Identicon Requirements
1. The identicon's should be symmetrical meaning the left horizontal half is equal to the right horizontal half.
2. The identicon is 5X5 pixels, following the standard specified for [GitHub identicons](https://github.blog/2013-08-14-identicons/)
3. Identicon's should use accessible colors as specified by [W3](https://www.w3.org/WAI/WCAG21/Techniques/general/G207)

## TODO:
- [ ] Finish script to implement identicon
- [ ] Implement core logic to generate a Python PIL or Tinkr image
- [ ] Write baseline tests
- [ ] Add CI/CD with GitHub actions to run tests
