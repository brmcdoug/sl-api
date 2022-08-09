# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import sl_bfd_common_pb2 as sl__bfd__common__pb2
import sl_bfd_ipv4_pb2 as sl__bfd__ipv4__pb2


class SLBfdv4OperStub(object):
  """@defgroup SLBfdIPv4Oper
  @ingroup BFD
  Used for IPv4 BFD registrations, and BFD session operations and notifications.
  Defines the RPC for adding, deleting, updating, and retrieving BFD sessions.
  @{
  @addtogroup SLBfdIPv4Oper
  @{
  ;
  BFD Registration Operations.

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SLBfdv4RegOp = channel.unary_unary(
        '/service_layer.SLBfdv4Oper/SLBfdv4RegOp',
        request_serializer=sl__bfd__common__pb2.SLBfdRegMsg.SerializeToString,
        response_deserializer=sl__bfd__common__pb2.SLBfdRegMsgRsp.FromString,
        )
    self.SLBfdv4Get = channel.unary_unary(
        '/service_layer.SLBfdv4Oper/SLBfdv4Get',
        request_serializer=sl__bfd__common__pb2.SLBfdGetMsg.SerializeToString,
        response_deserializer=sl__bfd__common__pb2.SLBfdGetMsgRsp.FromString,
        )
    self.SLBfdv4GetStats = channel.unary_unary(
        '/service_layer.SLBfdv4Oper/SLBfdv4GetStats',
        request_serializer=sl__bfd__common__pb2.SLBfdGetMsg.SerializeToString,
        response_deserializer=sl__bfd__common__pb2.SLBfdGetStatsMsgRsp.FromString,
        )
    self.SLBfdv4GetNotifStream = channel.unary_stream(
        '/service_layer.SLBfdv4Oper/SLBfdv4GetNotifStream',
        request_serializer=sl__bfd__common__pb2.SLBfdGetNotifMsg.SerializeToString,
        response_deserializer=sl__bfd__ipv4__pb2.SLBfdv4Notif.FromString,
        )
    self.SLBfdv4SessionOp = channel.unary_unary(
        '/service_layer.SLBfdv4Oper/SLBfdv4SessionOp',
        request_serializer=sl__bfd__ipv4__pb2.SLBfdv4Msg.SerializeToString,
        response_deserializer=sl__bfd__ipv4__pb2.SLBfdv4MsgRsp.FromString,
        )
    self.SLBfdv4SessionGet = channel.unary_unary(
        '/service_layer.SLBfdv4Oper/SLBfdv4SessionGet',
        request_serializer=sl__bfd__ipv4__pb2.SLBfdv4GetMsg.SerializeToString,
        response_deserializer=sl__bfd__ipv4__pb2.SLBfdv4GetMsgRsp.FromString,
        )


class SLBfdv4OperServicer(object):
  """@defgroup SLBfdIPv4Oper
  @ingroup BFD
  Used for IPv4 BFD registrations, and BFD session operations and notifications.
  Defines the RPC for adding, deleting, updating, and retrieving BFD sessions.
  @{
  @addtogroup SLBfdIPv4Oper
  @{
  ;
  BFD Registration Operations.

  """

  def SLBfdv4RegOp(self, request, context):
    """SLBfdRegMsg.Oper = SL_REGOP_REGISTER:
    Global BFD registration.
    A client Must Register BEFORE BFD sessions can be added/modified.

    SLBfdRegMsg.Oper = SL_REGOP_UNREGISTER:
    Global BFD un-registration.
    This call is used to end all BFD notifications and unregister any
    interest in BFD session configuration.
    This call cleans up all BFD sessions previously requested.

    SLBfdRegMsg.Oper = SL_REGOP_EOF:
    BFD End Of File.
    After Registration, the client is expected to send an EOF
    message to convey the end of replay of the client's known objects.
    This is especially useful under certain restart scenarios when the
    client and the server are trying to synchronize their BFD sessions.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SLBfdv4Get(self, request, context):
    """Used to retrieve global BFD info from the server.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SLBfdv4GetStats(self, request, context):
    """Used to retrieve global BFD stats from the server.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SLBfdv4GetNotifStream(self, request, context):
    """
    BFD notifications


    This call is used to get a stream of session state notifications.
    The caller must maintain the GRPC channel as long as
    there is interest in BFD session notifications. Only sessions that were
    created through this API will be notified to caller.
    This call can be used to get "push" notifications for session states.
    It is advised that the caller register for notifications before any
    sessions are created to avoid any loss of notifications.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SLBfdv4SessionOp(self, request, context):
    """
    BFD session operations


    SLBfdv4Msg.Oper = SL_OBJOP_ADD:
    Add one or multiple BFD sessions.

    SLBfdv4Msg.Oper = SL_OBJOP_UPDATE:
    Update one or multiple BFD sessions.

    SLBfdv4Msg.Oper = SL_OBJOP_DELETE:
    Delete one or multiple BFD sessions.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SLBfdv4SessionGet(self, request, context):
    """Retrieve BFD session attributes and state.
    This call can be used to "poll" the current state of a session.
    @}
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SLBfdv4OperServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SLBfdv4RegOp': grpc.unary_unary_rpc_method_handler(
          servicer.SLBfdv4RegOp,
          request_deserializer=sl__bfd__common__pb2.SLBfdRegMsg.FromString,
          response_serializer=sl__bfd__common__pb2.SLBfdRegMsgRsp.SerializeToString,
      ),
      'SLBfdv4Get': grpc.unary_unary_rpc_method_handler(
          servicer.SLBfdv4Get,
          request_deserializer=sl__bfd__common__pb2.SLBfdGetMsg.FromString,
          response_serializer=sl__bfd__common__pb2.SLBfdGetMsgRsp.SerializeToString,
      ),
      'SLBfdv4GetStats': grpc.unary_unary_rpc_method_handler(
          servicer.SLBfdv4GetStats,
          request_deserializer=sl__bfd__common__pb2.SLBfdGetMsg.FromString,
          response_serializer=sl__bfd__common__pb2.SLBfdGetStatsMsgRsp.SerializeToString,
      ),
      'SLBfdv4GetNotifStream': grpc.unary_stream_rpc_method_handler(
          servicer.SLBfdv4GetNotifStream,
          request_deserializer=sl__bfd__common__pb2.SLBfdGetNotifMsg.FromString,
          response_serializer=sl__bfd__ipv4__pb2.SLBfdv4Notif.SerializeToString,
      ),
      'SLBfdv4SessionOp': grpc.unary_unary_rpc_method_handler(
          servicer.SLBfdv4SessionOp,
          request_deserializer=sl__bfd__ipv4__pb2.SLBfdv4Msg.FromString,
          response_serializer=sl__bfd__ipv4__pb2.SLBfdv4MsgRsp.SerializeToString,
      ),
      'SLBfdv4SessionGet': grpc.unary_unary_rpc_method_handler(
          servicer.SLBfdv4SessionGet,
          request_deserializer=sl__bfd__ipv4__pb2.SLBfdv4GetMsg.FromString,
          response_serializer=sl__bfd__ipv4__pb2.SLBfdv4GetMsgRsp.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'service_layer.SLBfdv4Oper', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))