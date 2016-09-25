# -*- coding:utf-8 -*-

from flask import Blueprint, request, redirect, jsonify, url_for, render_template
from . import app
from vsphere_service import VsphereService
from vsphere_client import VsphereClient
from decorator.user import login_required,privilege
from decorator.vsphere import get_last_version

vsphereProfile = Blueprint('vsphereProfile', __name__)

vsphereService = VsphereService()
vsphereClient = VsphereClient()


@app.route('/vsphere/performance/json',methods=['GET'])
@login_required()
@privilege('vsphere')
def vsphere_performance_json():
    moid = request.args.get('moid')
    histlevel = request.args.get('histlevel')
    perftype = request.args.get('type')
    if moid and histlevel and perftype:
        perfinfo = vsphereClient.get_brief_performance(moid, histlevel, perftype)
        return jsonify(perfinfo)
    else:
        return 'bad request', 401


@app.route('/vsphere/performance/detail',methods=['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_performance_detail(version):
    ver = version.id
    if not request.args.get('type'):
        return redirect(url_for('vsphere_vm_home'))
    if not request.args.get('moid'):
        return redirect(url_for('vsphere_vm_home'))
    moid = request.args.get('moid')
    perftype = request.args.get('type')
    histlevel = request.args.get('histlevel')
    if histlevel == 'day':
        histlevelstr = u'近一日'
    elif histlevel == 'week':
        histlevelstr = u'近一周'
    elif histlevel == 'month':
        histlevelstr = u'近一月'
    else:
        histlevelstr = u'准实时'
    if perftype=='vm':
        info = vsphereService.get_brief_vminfo_by_vmid(ver, moid)
        ret = vsphereClient.get_performance(moid, histlevel, 'vm')
    elif perftype=='host':
        info = vsphereService.get_brief_hostinfo_by_hostid(ver, moid)
        ret = vsphereClient.get_performance(moid, histlevel, 'host')
    if ret:
        sampletime = ret['sampletime']
        cpuval = ret['cpuval']
        disk1val = ret['disk1val']
        disk2val = ret['disk2val']
        memval = ret['memval']
        netval = ret['netval']
        slen = len(sampletime)
        return render_template('vsphere/vsphere_performance_detail.html', title='VSpher VM Performance', sampletime=sampletime,
                               cpuval=cpuval, disk1val=disk1val, disk2val=disk2val, memval=memval, netval=netval,
                               slen=slen, info=info, histlevelstr=histlevelstr, moid=moid, perftype=perftype)
    else:
        return redirect(url_for('vsphere_vm_home'))


@app.route('/vsphere/host/detail',methods=['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_host_detail(version):
    if not request.args.get('hostid'):
        return redirect(url_for('vsphere_host_list'))
    hostid = request.args.get('hostid')
    ver = version.id
    hostinfo = vsphereService.get_host_detail_by_hostid(ver, hostid)
    return render_template('vsphere/vsphere_host_detail.html', title='VSpher Host', version=version, hostinfo=hostinfo)


@app.route('/vsphere/host',methods=['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_host_home(version):
    domainid = request.args.get('domainid')
    ver = version.id
    hostinfo = vsphereService.get_host_list_by_domainid(ver, domainid)
    domains = vsphereService.get_host_domain_list(ver)

    return render_template('vsphere/vsphere_host_home.html', title='VSpher Host List', version=version,
                           hostinfo=hostinfo, domains=domains, domain=domainid)



@app.route('/vsphere/datastore')
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_datastore_home(version):
    ver = version.id
    datastoreinfo = vsphereService.get_all_datastore(ver)
    return render_template('vsphere/vsphere_datastore_home.html', title='VSpher Datastore List', version=version,
                           datastoreinfo=datastoreinfo)


@app.route('/vsphere/network/detail',methods = ['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_network_detail(version):
    if not request.args.get('networkid'):
        return redirect(url_for('vsphere_network_home'))
    networkid = request.args.get('networkid')
    ver = version.id
    network = vsphereService.get_networkinfo_by_networkid(ver, networkid)
    return render_template('vsphere/vsphere_network_detail.html', title='VSpher Network List', version=version,
                           network=network)


@app.route('/vsphere/network',methods = ['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_network_home(version):
    ver = version.id
    networks = vsphereService.get_all_networks(ver)
    return render_template('vsphere/vsphere_network_home.html', title='VSpher Network', version=version, networks=networks)


@app.route('/vsphere/vm/map',methods=['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_vm_map(version):
    dcid = request.args.get('dcid', 'datacenter-2')
    ver = version.id
    dcmap = vsphereService.get_vm_map(ver, dcid)
    return render_template('vsphere/vsphere_vm_map.html', title='VSpher VM Map', version=version, dcmap=dcmap)


@app.route('/vsphere/project/map',methods=['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_project_map(version):
    dcid = request.args.get('dcid', 'datacenter-2')
    ver = version.id
    dcmap = vsphereService.get_project_map(ver, dcid)
    return render_template('vsphere/vsphere_project_map.html', title='VSpher Project Map', version=version, dcmap=dcmap)


@app.route('/vsphere/vm/detail',methods = ['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_vm_detail(version):
    if not request.args.get('vmid'):
        return redirect(url_for('vsphere_vm_home'))
    vmid = request.args.get('vmid')
    ver = version.id
    info = vsphereService.get_vm_detail_from_vmid(ver, vmid)
    zoneinfo = info['zone']
    projectinfo = info['project']
    vminfo = info['vm']
    vmnicinfo = info['vmnic']
    hostinfo = info['host']
    return render_template('vsphere/vsphere_vm_detail.html', title='VSpher VM', version=version, zoneinfo=zoneinfo, projectinfo=projectinfo,
                           vminfo=vminfo, vmnicinfo=vmnicinfo, hostinfo=hostinfo)


@app.route('/vsphere/vm/list',methods = ['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_vm_list(version):
    if not request.args.get('vmfid'):
        return redirect(url_for('vsphere_vm_home'))
    vmfid=request.args.get('vmfid')
    ver = version.id
    folder = vsphereService.get_folder(ver, vmfid)
    vms = vsphereService.get_child_vm(ver, vmfid)
    return render_template('vsphere/vsphere_vm_list.html', title='VSpher VM List', version=version, folder=folder, vms=vms)


@app.route('/vsphere/vm/project/list',methods = ['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_project_list(version):
    if not request.args.get('vmfid'):
        return redirect(url_for('vsphere_vm_home'))
    vmfid=request.args.get('vmfid')
    ver = version.id
    folders = vsphereService.get_project_list(ver, vmfid)
    return render_template('vsphere/vsphere_project_list.html', title='VSpher Project List', version=version,
                           folders=folders)


@app.route('/vsphere/vm', methods = ['GET'])
@login_required()
@privilege('vsphere')
@get_last_version()
def vsphere_vm_home(version):
    dcid = request.args.get('dcid','datacenter-2')
    ver = version.id
    dcs = vsphereService.get_all_datacenters(ver)
    dcinfo = vsphereService.get_dcinfo_by_dcid(ver, dcid)
    return render_template('vsphere/vsphere_vm_home.html', title='VSpher VM Home', version=version, dcs=dcs, dcinfo=dcinfo, dcid=dcid )

