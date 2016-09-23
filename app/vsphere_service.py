# -*- coding:utf-8 -*-

from model import db

from model.vsphere.datacenter import Datacenter
from model.vsphere.datacenter_folder import DatacenterFolder
from model.vsphere.datastore import Datastore
from model.vsphere.folder import Folder
from model.vsphere.host import Host
from model.vsphere.network import Network
from model.vsphere.version import Version
from model.vsphere.vm import VM
from model.vsphere.vmnic import VMNic

from IPy import IP

from sqlalchemy import desc

class VsphereService:

    def __init__(self):
        pass

    @staticmethod
    def saveVM(ver, vmid, name, parentid, parent, state, cpu, memory, os, committed, uncommitted, datastoreid, datastore):
        v = VM(version=ver, vmid=vmid, name=name, parentid=parentid, parent=parent, state=state, cpu=cpu, memory=memory, os=os,
               committed=committed, uncommitted=uncommitted, datastoreid=datastoreid, datastore=datastore)
        db.session.add(v)
        db.session.commit()

    @staticmethod
    def saveVMNic(ver, nicid, vmid, networktype, networkid, ipaddress, mac):
        vn = VMNic(version=ver, nicid=nicid, vmid=vmid, networktype=networktype, networkid=networkid, ipaddress=ipaddress, mac=mac)
        db.session.add(vn)
        db.session.commit()

    @staticmethod
    def saveDataCenter(ver, mid, name):
        d = Datacenter(version=ver,id=mid,name=name)
        db.session.add(d)
        db.session.commit()

    @staticmethod
    def saveFolder(ver, folderid, name, parentid, parent, ftype):
        f = Folder(version=ver, folderid=folderid, name=name, parentid=parentid, parent=parent, type=ftype)
        db.session.add(f)
        db.session.commit()

    @staticmethod
    def saveHost(ver, hostid, name, parentid, parent, cpu, memory, vendor, model):
        h = Host(version=ver, hostid=hostid, name=name, parentid=parentid, parent=parent, cpu=cpu, memory=memory, vendor=vendor, model=model)
        db.session.add(h)
        db.session.commit()

    @staticmethod
    def updateVMHost(ver, vmid, hostid):
        v = VM.query.get([ver,vmid])
        v.hostid = hostid
        db.session.commit()

    @staticmethod
    def saveNetwork(ver, networkid, name, parentid, parent, networktype):
        n = Network(version=ver, networkid=networkid, name=name, parentid=parentid, parent=parent, networktype=networktype)
        db.session.add(n)
        db.session.commit()

    @staticmethod
    def saveDatastore(ver, datastoreid, name, parentid, parent, capacity, freespace, uncommitted):
        d = Datastore(version=ver, datastoreid=datastoreid, name=name, parentid=parentid, parent=parent, capacity=capacity,
                      freespace=freespace, uncommitted=uncommitted)
        db.session.add(d)
        db.session.commit()

    @staticmethod
    def saveVersion():
        v = Version()
        db.session.add(v)
        db.session.commit()
        return v.id

    @staticmethod
    def saveDataCenterFolder(ver, folderid, name, datacenterid, datacenter, ftype):
        df = DatacenterFolder(version=ver, folderid=folderid, name=name, datacenterid=datacenterid, datacenter=datacenter, type=ftype)
        db.session.add(df)
        db.session.commit()

    @staticmethod
    def get_new_version():
        return Version.query.order_by(desc(Version.synctime)).first()

    @staticmethod
    def get_all_datacenters(ver):
        return Datacenter.query.filter(Datacenter.version==ver).all()

    @staticmethod
    def get_dcinfo_by_dcid(ver, dcid):
        ret = dict();
        dc = Datacenter.query.get([ver, dcid])
        ret['name'] = dc.name
        ret['id'] = dc.id
        ret['zone'] = list()
        dcfs = DatacenterFolder.query.filter(DatacenterFolder.version == ver, DatacenterFolder.datacenterid == dc.id).all()
        for dcf in dcfs:
            fs = Folder.query.filter(Folder.version==ver, Folder.parentid==dcf.folderid)
            for f in fs:
                count = Folder.query.filter(Folder.version==ver, Folder.parentid==f.folderid).count()
                zone = dict()
                zone['name'] = f.name
                zone['id'] = f.folderid
                zone['members'] = count
                ret['zone'].append(zone)
        return ret

    @staticmethod
    def get_project_list(ver, vmfid):
        ret = dict()
        pf = Folder.query.get([ver,vmfid])
        ret['name'] = pf.name
        ret['id'] = pf.folderid
        cfs = Folder.query.filter(Folder.version==ver, Folder.parentid==pf.folderid)
        ret['project_number'] = cfs.count()
        ret['folders'] = list()
        vms = VM.query.filter(VM.version == ver, VM.parentid == pf.folderid)
        ret['unclassified'] = vms.count()
        vm_numbers = vms.count()
        for cf in cfs:
            vms = VM.query.filter(VM.version==ver, VM.parentid==cf.folderid)
            f = dict()
            f['name'] = cf.name
            f['id'] = cf.folderid
            f['members'] = vms.count()
            vm_numbers += vms.count()
            ret['folders'].append(f)
        ret['vm_number'] = vm_numbers
        return ret

    @staticmethod
    def get_folder(ver, vmfid):
        return Folder.query.get([ver,vmfid])

    @staticmethod
    def get_child_vm(ver, vmfid):
        return VM.query.filter(VM.version==ver, VM.parentid==vmfid).all()

    @staticmethod
    def get_vm_detail_from_vmid(ver, vmid):
        ret = dict()
        vm = VM.query.get([ver, vmid])
        project = Folder.query.get([ver,vm.parentid])
        zone = Folder.query.get([ver,project.parentid])
        if not zone:
            zone = project
            project = None
        vmnic = VMNic.query.filter(VMNic.version==ver,VMNic.vmid==vmid).all()
        host = Host.query.get([ver,vm.hostid])
        ret['zone'] = zone
        ret['project'] = project
        ret['vm'] = vm
        ret['vmnic'] = vmnic
        ret['host'] = host
        return ret

    @staticmethod
    def get_project_map(ver, dcid):
        ret = dict();
        dc = Datacenter.query.get([ver, dcid])
        ret['name'] = dc.name
        ret['zone'] = list()
        dcfs = DatacenterFolder.query.filter(DatacenterFolder.version == ver,
                                             DatacenterFolder.datacenterid == dc.id).all()
        for dcf in dcfs:
            zs = Folder.query.filter(Folder.version == ver, Folder.parentid == dcf.folderid)
            for z in zs:
                zone = dict()
                zone['name'] = z.name
                zone['id'] = z.folderid
                zone['project'] = list()
                ps = Folder.query.filter(Folder.version == ver, Folder.parentid == z.folderid).all()
                for p in ps:
                    project = dict()
                    project['id'] = p.folderid
                    project['name'] = p.name
                    zone['project'].append(project)
                zone['members'] = len(ps)
                ret['zone'].append(zone)
        return ret

    @staticmethod
    def get_vm_map(ver, dcid):
        ret = dict();
        dc = Datacenter.query.get([ver, dcid])
        ret['name'] = dc.name
        ret['zone'] = list()
        dcfs = DatacenterFolder.query.filter(DatacenterFolder.version == ver,
                                             DatacenterFolder.datacenterid == dc.id).all()
        for dcf in dcfs:
            zs = Folder.query.filter(Folder.version == ver, Folder.parentid == dcf.folderid)
            for z in zs:
                zone = dict()
                zone['name'] = z.name
                zone['id'] = z.folderid
                zone['project'] = list()
                ps = Folder.query.filter(Folder.version == ver, Folder.parentid == z.folderid).all()
                for p in ps:
                    project = dict()
                    project['id'] = p.folderid
                    project['name'] = p.name
                    project['vms'] = list()
                    vms = VM.query.filter(VM.version == ver, VM.parentid == p.folderid).all()
                    for vm in vms:
                        v = dict()
                        v['name'] = vm.name
                        v['id'] = vm.vmid
                        project['vms'].append(v)
                    zone['project'].append(project)
                ret['zone'].append(zone)
        return ret

    @staticmethod
    def get_all_networks(ver):
        ret = list()
        ns = Network.query.filter(Network.version == ver)
        for n in ns:
            l = dict()
            l['id'] = n.networkid
            l['name'] = n.name
            l['type'] = n.networktype
            l['count'] = VMNic.query.filter(VMNic.version == ver, VMNic.networkid == n.networkid).count()
            ret.append(l)
        return ret

    @staticmethod
    def get_networkinfo_by_networkid(ver, networkid):
        networkinfo = Network.query.get([ver,networkid])
        if networkinfo:
            vmnics = VMNic.query.filter(VMNic.version == ver, VMNic.networkid == networkid).all()
            knownnetwork = dict()
            unknownnetwork = list()
            ret = {}
            for vmnic in vmnics:
                ip = vmnic.ipaddress
                if ip:
                    if ip[0:7] == '198.15.':
                        ret['net'] = IP(ip).make_net('255.255.252.0')
                        for i in range(0, 4):
                            for j in range(1, 255):
                                r = dict()
                                r['ipsquence'] = i*1000+j
                                knownnetwork['198.15.'+str(i)+'.'+str(j)] = r
                    else:
                        ret['net'] = IP(ip).make_net('255.255.255.0')
                        net = IP(ip).make_net('255.255.255.0').net().strNormal()
                        net = net[0:net.rfind('.')]
                        for i in range(1, 255):
                            r = dict()
                            r['ipsquence'] = i
                            knownnetwork[net + '.' + str(i)] = r
                    break
            known = 0
            for vmnic in vmnics:
                vm = VM.query.get([ver,vmnic.vmid])
                project = Folder.query.get([ver, vm.parentid])
                zone = Folder.query.get([ver, project.parentid])
                if not zone:
                    zone = project
                    project = None
                ip = vmnic.ipaddress
                r = knownnetwork.get(ip)
                if not r:
                    r = dict()
                    ip = None

                r['id'] = vm.vmid
                r['name'] = vm.name
                r['zid'] = zone.folderid
                r['zname'] = zone.name
                if project:
                    r['pid'] = project.folderid
                    r['pname'] = project.name

                if ip:
                    known += 1
                    knownnetwork[ip] = r
                    print r
                else:
                    unknownnetwork.append(r)
            ret['known'] = known
            ret['knownnetwork'] = knownnetwork
            ret['unknownnetwork'] = unknownnetwork
            ret['name'] = networkinfo.name
            ret['type'] = networkinfo.networktype

            print ret
            return ret

    @staticmethod
    def get_all_datastore(ver):
        ds = Datastore.query.filter(Datastore.version == ver)
        ret = list()
        for d in ds:
            if d.name[0:9] != 'datastore':
                ret.append(d)
        return ret

    @staticmethod
    def get_host_list_by_domainid(ver, domainid):
        hs = Host.query.filter(Host.version == ver, Host.parentid == domainid if domainid else "")
        ret = list()
        for h in hs:
            r = dict()
            vms = VM.query.filter(VM.version == ver, VM.hostid == h.hostid)
            cpu = 0
            mem = 0
            count = 0
            for vm in vms:
                if vm.state=='poweredOn':
                    count += 1
                    cpu += vm.cpu
                    mem += vm.memory
            r['id'] = h.hostid
            r['name'] = h.name
            r['domainid'] = h.parentid
            r['domain'] = h.parent
            r['hcpu'] = h.cpu
            r['hmem'] = h.memory
            r['vcpu'] = cpu
            r['vmem'] = mem
            r['vmcount'] = count
            ret.append(r)
        return ret

    @staticmethod
    def get_host_domain_list(ver):
        hs = Host.query.filter(Host.version == ver)
        ret =dict()
        for h in hs:
            ret[h.parentid] = h.parent
        return ret

    @staticmethod
    def get_host_detail_by_hostid(ver, hostid):
        h = Host.query.get([ver,hostid])
        ret = dict()
        if h:
            ret['id'] = h.hostid
            ret['name'] = h.name
            ret['domainid'] = h.parentid
            ret['domain'] = h.parent
            ret['cpu'] = h.cpu
            ret['mem'] = h.memory
            ret['vendor'] = h.vendor
            ret['model'] = h.model
            vms = VM.query.filter(VM.version == ver, VM.hostid == h.hostid)
            vcpu = 0
            vmem = 0
            ret['vms'] = list()
            for vm in vms:
                if vm.state == 'poweredOn':
                    vcpu += vm.cpu
                    vmem += vm.memory
                ret['vms'].append(vm)
            ret['vcpu'] = vcpu
            ret['vmem'] = vmem
            return ret

    @staticmethod
    def get_brief_vminfo_by_vmid(ver, vmid):
        return VM.query.get([ver, vmid])

    @staticmethod
    def get_brief_hostinfo_by_hostid(ver, hostid):
        return Host.query.get([ver, hostid])
