def get_vm_hostnames():
    ns = { 'url': 'http://openstack.org/xmlns/libvirt/nova/1.0' }
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system')
        exit(1)
    index = 0 
    vms = {}
    for i in conn.listAllDomains():
      vms[index] = {}
      raw_xml = i.XMLDesc(0)
      root = ET.fromstring(raw_xml)
      for child in root.findall('metadata'):
        for c in child.findall('url:instance', ns):
          for cc in c:
            if cc.tag == '{%s}name' % ns['url']:
              vms[index]['hostname'] = cc.text
            if cc.tag == '{%s}creationTime' % ns['url']:
              vms[index]['creationTime'] = cc.text
            if cc.tag == '{%s}flavor' % ns['url']:
              vms[index]['flavor'] = cc.attrib['name']
            if cc.tag == '{%s}owner' % ns['url']:
              vms[index]['owner'] = cc.find('url:user', ns).text
            if cc.tag == '{%s}owner' % ns['url']:
              vms[index]['project'] = cc.find('url:project', ns).text
      index = index + 1
    output = ''
    for v in vms:
      output = output + "instance_%s.hostname=%s " % (v, vms[v]['hostname'])
      output = output + "instance_%s.creationTime=%s " % (v, '-'.join(vms[v]['creationTime'].split()))
      output = output + "instance_%s.flavor=%s " % (v, vms[v]['flavor'])
      output = output + "instance_%s.owner=%s " % (v, vms[v]['owner'])
      output = output + "instance_%s.project=%s " % (v, vms[v]['project'])
    return output 
