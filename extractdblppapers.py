import xml.sax
import msgpack
 
elems = set(["title", "author", "year", "booktitle", "journal", "crossref"])

class ABContentHandler(xml.sax.ContentHandler):
  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
    self.depth = 0
    self.structure = None
    self.tag = None
    self.all = []
    self.count = 0
 
  def startElement(self, name, attrs):
    self.depth += 1
    if self.depth == 2:
      # Start a new strucure
      self.structure = {}

      try:
        if name == "article":
          if attrs.getValue("publtype"):
             self.structure = None
      except:
        pass

    elif self.depth == 3:
      if self.structure is not None and name in elems:
        if name not in self.structure:
          self.structure[name] = []
          self.tag = name

    # print("startElement '" + name + "', " + str(self.depth))
    
  def endElement(self, name):
    # print("endElement '" + name + "'")
    self.depth -= 1
    if self.tag:
      self.tag = None
 
    if self.depth == 1:
      if self.structure is not None and "author" in self.structure and "year" in self.structure:
        if int(self.structure["year"][0]) >= 2005:
          # print self.structure

          # Massage a bit the structure
          B = None
          if "booktitle" in self.structure:
            B = self.structure["booktitle"][0]
          elif "journal" in self.structure:
            B = self.structure["journal"][0]

          rec = (self.structure["author"], \
              self.structure["title"][0], \
              B, int(self.structure["year"][0]))

          self.all += [rec]
          self.count += 1
          if self.count % 10000 == 0:
            print self.count

  def characters(self, content):
    # print("characters '" + content + "'")
    if self.tag:
      self.structure[self.tag] += [content]
 
 
if __name__ == "__main__":
  source = open("dblp.xml")
  data = ABContentHandler()
  xml.sax.parse(source, data)

  packed_data = msgpack.packb(data.all, use_bin_type=True)
  file("allfiles.dat", "wb").write(packed_data)