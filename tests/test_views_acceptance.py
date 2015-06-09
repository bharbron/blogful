import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
  def setUp(self):
    """ Test setup """
    self.browser = Browser("phantomjs")
    
    # Set up the tables in the database
    Base.metadata.create_all(engine)
    
    # Create an example user
    self.user = models.User(name="Alice", email="alice@example.com", password=generate_password_hash("test"))
    session.add(self.user)
    session.commit()
    
    # Create a second example user
    self.user2 = models.User(name="Carlos", email="carlos@example.com", password=generate_password_hash("test"))
    session.add(self.user2)
    session.commit()
    
    # Create some sample posts
    content = "A post for acceptance testing"
    for i in range (5):
      post = models.Post(title="Acceptance test post #{}".format(i+1), content=content, author=self.user)
      session.add(post)
    session.commit()
        
    self.process = multiprocessing.Process(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    self.process.start()
    time.sleep(1)
    
  def tearDown(self):
    """ Test teardown """
    # Remove the tables and their data from the database
    self.process.terminate()
    session.close()
    engine.dispose()
    Base.metadata.drop_all(engine)
    self.browser.quit()
    
  def testLoginCorrect(self):
    self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.fill("email", "alice@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
    
  def testLoginIncorrect(self):
    self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.fill("email", "bob@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")
    
  def testEditAsAuthor(self):
    self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.fill("email", "alice@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.browser.visit("http://0.0.0.0:8080/post/2/edit")
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/post/2/edit")
    self.browser.fill("title", "edited title")
    self.browser.fill("content", "edited content")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/post/2")
    self.assertTrue(self.browser.is_text_present("edited title"))
    self.assertTrue(self.browser.is_text_present("edited content"))
  
  def testEditNotAsAuthor(self):
    self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.fill("email", "carlos@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.browser.visit("http://0.0.0.0:8080/post/1/edit")
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
  
  def testDeleteAsAuthor(self):
    self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.fill("email", "alice@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.browser.visit("http://0.0.0.0:8080/post/1/delete")
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/post/1/delete")
  
  def testDeleteNotAsAuthor(self):
    self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.fill("email", "carlos@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    self.browser.visit("http://0.0.0.0:8080/post/1/delete")
    self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
    
if __name__ == "__main__":
  unittest.main()