========
Overview
========

This archive contains the testing corpus for the "Sexual Predator Identification" task of the PAN 2012 Lab, held in conjunction with the CLEF 2012 conference.

Find out about all the details at http://pan.webis.de.



===========================
Testing Corpus Description
===========================

The corpus comprises:

pan12-sexual-predator-identification-test-2012-05-17 The xml file containing around 155000 documents (each document is a conversation)

The xml file is organized as follow (identically to the training set):
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

Given the public nature of the dataset, we ask the participants not to use external or online resources for resolving this task (e.g. search engines) but to extract evidence from the provided datasets only. 


==========
Contacts
==========

In case of problem with the corpus, you can write directly to Giacomo Inches at giacomo.inches@usi.ch
