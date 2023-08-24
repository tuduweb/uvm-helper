#/bin/python3

demostr = """
-----------------------------------------------------------------
Name                        Type             Size  Value         
-----------------------------------------------------------------
bin_eth_pkt                 bin_eth_pkt      -     -             
  src_port                  integral         2     'h0           
  dst_port                  integral         2     'h0           
  dmac                      integral         48    'h0           
  smac                      integral         48    'h0           
  is_with_vlan_tag          integral         2     'h0           
  vlan_tag                  VLAN_Tag         -     -             
    tpid                    integral         16    'h0           
    pri                     integral         3     'h0           
    cfi                     integral         1     'h0           
    vid                     integral         12    'h0           
  ethertype_or_length_data  integral         16    'h0           
  llc                       LLC              -     -             
    llc_dsap                integral         8     'h0           
    llc_ssap                integral         8     'h0           
    llc_control             integral         8     'h0           
  snap                      SNAP             -     -             
    oui                     integral         24    'h0           
    protocol_id             integral         16    'h0           
  expect_pack_type          pkt_pack_type_e  3     PKT_PT_DEFAULT
  expect_ether_type         pkt_ethertype_e  8     PKT_ET_DEFAULT
  pkt_pack_type             pkt_pack_type_e  3     PKT_PT_DEFAULT
  pkt_ether_type            pkt_ethertype_e  8     PKT_ET_DEFAULT
  length                    integral         32    'd0           
  expect_pkt_len            integral         32    'd0           
  pkt_len                   integral         32    'd0           
-----------------------------------------------------------------
"""

import re

class bin_eth_pkt(object):
    def __init__(self):
        pass



class uvm_field_item(object):
    field_name = ""
    filed_type = ""
    field_type_p1 = 0
    filed_value = None

    def __init__(self, _name, _type, _value):
        self.field_name     = _name
        self.field_type     = _type
        self.field_type_p1  = 1
        self.field_value    = _value
        pass

    def bits_pack(self):
        pass

    def bits_unpack(self, bits):
        pass

    def display(self):
        if isinstance(self.field_value, str):
            print("item", self.field_name, self.field_type, self.field_type_p1, self.field_value)
        elif isinstance(self.field_value, list):
            print("-"*40)
            print("block:[%s]" % self.field_name)
            print("-"*40)
            for item in self.field_value:
                item.display()


class uvm_field_block(uvm_field_item):
    childs = []
    
    def __init__(self, _name):
        super().__init__(_name, "field_block", [])

    def addChild(self, childItem):
        # self.field_value
        self.childs.append(childItem)
        self.field_value.append(childItem)
        pass

    # def display(self):
    #     print("-"*20)
    #     print("block", self.field_name)
    #     print("-"*20)

    #     for item in self.childs:
    #         item.display()

class pkt_reader(object):
    def __init__(self):
        pass

    def _parse_one(self, inputStr):
        dataLines = inputStr.splitlines()
        if len(dataLines) <= 3:
            pass

        print(len(inputStr.splitlines()))

        print("-" in set(inputStr.splitlines()[1]))

        pass


    def parse_fields(self, data):
        pattern = r'(\w+)\s+(\w+)\s+(\S+)\s+\'(.*)\''
        matches = re.findall(pattern, data)

        fields = []
        for match in matches:
            field_name = match[0]
            field_type = match[1]
            field_size = match[2]
            field_value = match[3]
            fields.append((field_name, field_value))

        return fields



if __name__ == "__main__":
    # print("hello world")

    reader = pkt_reader()
    reader._parse_one(demostr)

    fields = reader.parse_fields(demostr)
    print(fields)

    items = []
    
    block = uvm_field_block("demo block")
    
    for i in range(0, 20):
        item = uvm_field_item("item%d" % i, "integral", "'h%d" % (i * 3))
        # item.display()
        block.addChild(item)
    
    block.display()