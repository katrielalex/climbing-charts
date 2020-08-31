# climbing-charts

This is a simple AWS sandbox powering https://walls.katriel.co.uk. It does two things:

  1) scrapes the capacity data out of the Lakeland Climbing Centre live trackers into DynamoDB every five minutes, and
  2) serves it up on a silly JSON API.

This API is then consumed by public/index.html which renders it into some capacity charts.

# Making changes

To change walls.katriel.co.uk, just push changes to public/index.html and Netlify will serve a static website.

[![Netlify Status](https://api.netlify.com/api/v1/badges/40a98486-c7b1-4c52-8c86-d186b041682e/deploy-status)](https://app.netlify.com/sites/festive-visvesvaraya-dc7e58/deploys)

To change the AWS infra, edit the code locally then run `make deploy` to push it to prod. You can test the functions with the `make local-*` commands (so for example to test the frontend run `make local-serve` and then `cd public; python3 -m http.server; open localhost:8000`). Note that the DynamoDB backend is whatever you have in your docker container, so if you want better test data run `make local-scrape` a few times to populate it.
