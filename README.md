Revealjs to Essay
=================

A helper library to turn revealjs slides into an essay skeleton.  
See [here](https://github.com/hakimel/reveal.js/#instructions-1) for exporting to pdf.  Roughly,
add ?print-pdf to the url (for example, http://localhost:8000/?print-pdf), then use the system
print interface to make a pdf.

After that:
```
brew install poppler
git clone https://github.com/ColCarroll/reveal_to_essay.git
cd reveal_to_essay
pip install click
python reveal_to_essay.py --out-dir ~/cool_talk --pdf-name ~/Desktop/cooltalk_slides/cool.pdf
```

Uses `poppler` to convert pdfs to pngs.  See 
[this talk](https://colcarroll.github.io/hamiltonian_monte_carlo_talk/bayes_talk.html)
for what the template looks like.
