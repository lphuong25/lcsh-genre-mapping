This is a project of mapping subjects from LCSH into Netflix-like Genres for books at a library that use Alma with LCHS system

**Feature**
The program will extract the keywords from the subject headings and mapping them according to user's desire

**Mechanism**
- First we will load the file and clean the text from subjects column by lower() and remove spaces or _ (suggest using excel because csv might convert long MMSId number)
- At this step we get the unformatted subjects, but we have to remove double dash --, commas, etc to finalize the cleaning
- Now we get the cleaned subjects lines, we will remove any duplicate words inside subject, and boost important word that can easily be missed during the process by adding symnonyms
- At this point, we can print some samples of the outputs and look for names, locations, etc aka noisy word, so we will eliminate them at cleaning step
