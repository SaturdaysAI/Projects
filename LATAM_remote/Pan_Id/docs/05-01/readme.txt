========
Overview
========

This archive contains the training corpus for the "Sexual Predator Identification" task of the PAN 2012 Lab, held in conjunction with the CLEF 2012 conference.

Find out about all the details at http://pan.webis.de.



===========================
Training Corpus Description
===========================

Update 01 May 2012:

pan12-sexual-predator-identification-training-corpus-2012-05-01.xml A new xml file containing conversations without bad username substitution.
pan12-sexual-predator-identification-diff.txt A text file containing conversation id and line number of modified text 
pan12-sexual-predator-identification-training-corpus-predators-2012-05-01.txt The list of predators without the ones not present in the traininig set



The corpus comprises:

pan12-sexual-predator-identification-training-corpus.xml An xml file containing around 60000 documents (each document is a conversation)
pan12-sexual-predator-identification-training-corpus-predators.txt A file containing a list of predators id

The xml file is organized as follow:
<?xml version="1.0" encoding="UTF-8"?>
<conversations>
  <conversation id="id_of_the_conversation">
    <message line="1">
      <author>author_1_id</author>
      <time>02:56</time>
      <text>Bla bla bla bla</text>
    </message>
    <message line="2">
      <author>author_2_id</author>
      <time>02:56</time>
      <text>bla bla</text>
    </message>
[...]
    <message line="n">
      <author> author_1_id </author>
      <time>07:12</time>
      <text>bla bla bla</text>
    </message>
  </conversation>
</conversations>

Every conversation, identified by and unique id, contains a set of messages. Each message, identified by a line number unique in the conversation, is produced by an author, identified by the author_id. In each message there is the text produced by the user and a time indication.

Please note that time, user_id and email address have been processed as follows: 
- The time is formatted as hours:minutes (might not be the real time)
- The user_id replaces any mentioning of the user within the conversation
- The email addresses have been replaced with a tag <email/>

Despite the preprocessing performed on the documents contained in the dataset, we are not responsible for the content of the documents (e.g eventual personal informations that might be contained in the text).

The training is a representative sample of the testing dataset and should be considered a training in the sense of "practicing" set. 

The .txt file contains a list of user_id who are Sexual Predator.

Given the public nature of the dataset, we ask the participants not to use external or online resources for resolving this task (e.g. search engines) but to extract evidence from the provided datasets only. 


==========
Contacts
==========

In case of problem with the corpus, you can write directly to Giacomo Inches at giacomo.inches@usi.ch
