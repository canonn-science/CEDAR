const zlib = require('zlib');
const zmq = require('zeromq');
const sock = zmq.socket('sub');

sock.connect('tcp://cedar.canonn.tech:9500');
console.log('Worker connected to port 9500');

sock.subscribe('');

sock.on('message', topic => {
  console.log(JSON.parse(zlib.inflateSync(topic)));
});
