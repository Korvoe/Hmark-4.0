// Code generated by protoc-gen-gogo. DO NOT EDIT.
// source: geo/geoindex/config.proto

package geoindex

import proto "github.com/gogo/protobuf/proto"
import fmt "fmt"
import math "math"

import encoding_binary "encoding/binary"

import io "io"

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.GoGoProtoPackageIsVersion2 // please upgrade the proto package

// Config is the information used to tune one instance of a geospatial index.
// Each SQL index will have its own config.
//
// At the moment, only one major indexing strategy is implemented (S2 cells).
type Config struct {
	S2Geography *S2GeographyConfig `protobuf:"bytes,1,opt,name=s2_geography,json=s2Geography,proto3" json:"s2_geography,omitempty"`
	S2Geometry  *S2GeometryConfig  `protobuf:"bytes,2,opt,name=s2_geometry,json=s2Geometry,proto3" json:"s2_geometry,omitempty"`
}

func (m *Config) Reset()         { *m = Config{} }
func (m *Config) String() string { return proto.CompactTextString(m) }
func (*Config) ProtoMessage()    {}
func (*Config) Descriptor() ([]byte, []int) {
	return fileDescriptor_config_4fdfa32e25381f1e, []int{0}
}
func (m *Config) XXX_Unmarshal(b []byte) error {
	return m.Unmarshal(b)
}
func (m *Config) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	b = b[:cap(b)]
	n, err := m.MarshalTo(b)
	if err != nil {
		return nil, err
	}
	return b[:n], nil
}
func (dst *Config) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Config.Merge(dst, src)
}
func (m *Config) XXX_Size() int {
	return m.Size()
}
func (m *Config) XXX_DiscardUnknown() {
	xxx_messageInfo_Config.DiscardUnknown(m)
}

var xxx_messageInfo_Config proto.InternalMessageInfo

// S2Config is the required information to tune one instance of an S2 cell
// backed geospatial index. For advanced users only -- the defaults should be
// good enough.
//
// TODO(sumeer): Based on experiments, reduce the knobs below by making the
// covering self-tuning.
type S2Config struct {
	// MinLevel is the minimum cell level stored in the index. If left unset, it
	// defaults to 0.
	MinLevel int32 `protobuf:"varint,1,opt,name=min_level,json=minLevel,proto3" json:"min_level,omitempty"`
	// MaxLevel is the maximum cell level stored in the index. If left unset, it
	// defaults to 30.
	MaxLevel int32 `protobuf:"varint,2,opt,name=max_level,json=maxLevel,proto3" json:"max_level,omitempty"`
	// `MaxLevel-MinLevel` must be an exact multiple of LevelMod. If left unset,
	// it defaults to 1.
	LevelMod int32 `protobuf:"varint,3,opt,name=level_mod,json=levelMod,proto3" json:"level_mod,omitempty"`
	// MaxCells is a soft hint for the maximum number of entries used to store a
	// single geospatial object. If left unset, it defaults to 4.
	MaxCells int32 `protobuf:"varint,4,opt,name=max_cells,json=maxCells,proto3" json:"max_cells,omitempty"`
}

func (m *S2Config) Reset()         { *m = S2Config{} }
func (m *S2Config) String() string { return proto.CompactTextString(m) }
func (*S2Config) ProtoMessage()    {}
func (*S2Config) Descriptor() ([]byte, []int) {
	return fileDescriptor_config_4fdfa32e25381f1e, []int{1}
}
func (m *S2Config) XXX_Unmarshal(b []byte) error {
	return m.Unmarshal(b)
}
func (m *S2Config) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	b = b[:cap(b)]
	n, err := m.MarshalTo(b)
	if err != nil {
		return nil, err
	}
	return b[:n], nil
}
func (dst *S2Config) XXX_Merge(src proto.Message) {
	xxx_messageInfo_S2Config.Merge(dst, src)
}
func (m *S2Config) XXX_Size() int {
	return m.Size()
}
func (m *S2Config) XXX_DiscardUnknown() {
	xxx_messageInfo_S2Config.DiscardUnknown(m)
}

var xxx_messageInfo_S2Config proto.InternalMessageInfo

type S2GeographyConfig struct {
	S2Config *S2Config `protobuf:"bytes,1,opt,name=s2_config,json=s2Config,proto3" json:"s2_config,omitempty"`
}

func (m *S2GeographyConfig) Reset()         { *m = S2GeographyConfig{} }
func (m *S2GeographyConfig) String() string { return proto.CompactTextString(m) }
func (*S2GeographyConfig) ProtoMessage()    {}
func (*S2GeographyConfig) Descriptor() ([]byte, []int) {
	return fileDescriptor_config_4fdfa32e25381f1e, []int{2}
}
func (m *S2GeographyConfig) XXX_Unmarshal(b []byte) error {
	return m.Unmarshal(b)
}
func (m *S2GeographyConfig) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	b = b[:cap(b)]
	n, err := m.MarshalTo(b)
	if err != nil {
		return nil, err
	}
	return b[:n], nil
}
func (dst *S2GeographyConfig) XXX_Merge(src proto.Message) {
	xxx_messageInfo_S2GeographyConfig.Merge(dst, src)
}
func (m *S2GeographyConfig) XXX_Size() int {
	return m.Size()
}
func (m *S2GeographyConfig) XXX_DiscardUnknown() {
	xxx_messageInfo_S2GeographyConfig.DiscardUnknown(m)
}

var xxx_messageInfo_S2GeographyConfig proto.InternalMessageInfo

type S2GeometryConfig struct {
	// The rectangle bounds of the plane that will be efficiently indexed. Shapes
	// should rarely exceed these bounds.
	MinX     float64   `protobuf:"fixed64,1,opt,name=min_x,json=minX,proto3" json:"min_x,omitempty"`
	MaxX     float64   `protobuf:"fixed64,2,opt,name=max_x,json=maxX,proto3" json:"max_x,omitempty"`
	MinY     float64   `protobuf:"fixed64,3,opt,name=min_y,json=minY,proto3" json:"min_y,omitempty"`
	MaxY     float64   `protobuf:"fixed64,4,opt,name=max_y,json=maxY,proto3" json:"max_y,omitempty"`
	S2Config *S2Config `protobuf:"bytes,5,opt,name=s2_config,json=s2Config,proto3" json:"s2_config,omitempty"`
}

func (m *S2GeometryConfig) Reset()         { *m = S2GeometryConfig{} }
func (m *S2GeometryConfig) String() string { return proto.CompactTextString(m) }
func (*S2GeometryConfig) ProtoMessage()    {}
func (*S2GeometryConfig) Descriptor() ([]byte, []int) {
	return fileDescriptor_config_4fdfa32e25381f1e, []int{3}
}
func (m *S2GeometryConfig) XXX_Unmarshal(b []byte) error {
	return m.Unmarshal(b)
}
func (m *S2GeometryConfig) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	b = b[:cap(b)]
	n, err := m.MarshalTo(b)
	if err != nil {
		return nil, err
	}
	return b[:n], nil
}
func (dst *S2GeometryConfig) XXX_Merge(src proto.Message) {
	xxx_messageInfo_S2GeometryConfig.Merge(dst, src)
}
func (m *S2GeometryConfig) XXX_Size() int {
	return m.Size()
}
func (m *S2GeometryConfig) XXX_DiscardUnknown() {
	xxx_messageInfo_S2GeometryConfig.DiscardUnknown(m)
}

var xxx_messageInfo_S2GeometryConfig proto.InternalMessageInfo

func init() {
	proto.RegisterType((*Config)(nil), "cockroach.geo.geoindex.Config")
	proto.RegisterType((*S2Config)(nil), "cockroach.geo.geoindex.S2Config")
	proto.RegisterType((*S2GeographyConfig)(nil), "cockroach.geo.geoindex.S2GeographyConfig")
	proto.RegisterType((*S2GeometryConfig)(nil), "cockroach.geo.geoindex.S2GeometryConfig")
}
func (this *Config) Equal(that interface{}) bool {
	if that == nil {
		return this == nil
	}

	that1, ok := that.(*Config)
	if !ok {
		that2, ok := that.(Config)
		if ok {
			that1 = &that2
		} else {
			return false
		}
	}
	if that1 == nil {
		return this == nil
	} else if this == nil {
		return false
	}
	if !this.S2Geography.Equal(that1.S2Geography) {
		return false
	}
	if !this.S2Geometry.Equal(that1.S2Geometry) {
		return false
	}
	return true
}
func (this *S2Config) Equal(that interface{}) bool {
	if that == nil {
		return this == nil
	}

	that1, ok := that.(*S2Config)
	if !ok {
		that2, ok := that.(S2Config)
		if ok {
			that1 = &that2
		} else {
			return false
		}
	}
	if that1 == nil {
		return this == nil
	} else if this == nil {
		return false
	}
	if this.MinLevel != that1.MinLevel {
		return false
	}
	if this.MaxLevel != that1.MaxLevel {
		return false
	}
	if this.LevelMod != that1.LevelMod {
		return false
	}
	if this.MaxCells != that1.MaxCells {
		return false
	}
	return true
}
func (this *S2GeographyConfig) Equal(that interface{}) bool {
	if that == nil {
		return this == nil
	}

	that1, ok := that.(*S2GeographyConfig)
	if !ok {
		that2, ok := that.(S2GeographyConfig)
		if ok {
			that1 = &that2
		} else {
			return false
		}
	}
	if that1 == nil {
		return this == nil
	} else if this == nil {
		return false
	}
	if !this.S2Config.Equal(that1.S2Config) {
		return false
	}
	return true
}
func (this *S2GeometryConfig) Equal(that interface{}) bool {
	if that == nil {
		return this == nil
	}

	that1, ok := that.(*S2GeometryConfig)
	if !ok {
		that2, ok := that.(S2GeometryConfig)
		if ok {
			that1 = &that2
		} else {
			return false
		}
	}
	if that1 == nil {
		return this == nil
	} else if this == nil {
		return false
	}
	if this.MinX != that1.MinX {
		return false
	}
	if this.MaxX != that1.MaxX {
		return false
	}
	if this.MinY != that1.MinY {
		return false
	}
	if this.MaxY != that1.MaxY {
		return false
	}
	if !this.S2Config.Equal(that1.S2Config) {
		return false
	}
	return true
}
func (m *Config) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *Config) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	if m.S2Geography != nil {
		dAtA[i] = 0xa
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.S2Geography.Size()))
		n1, err := m.S2Geography.MarshalTo(dAtA[i:])
		if err != nil {
			return 0, err
		}
		i += n1
	}
	if m.S2Geometry != nil {
		dAtA[i] = 0x12
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.S2Geometry.Size()))
		n2, err := m.S2Geometry.MarshalTo(dAtA[i:])
		if err != nil {
			return 0, err
		}
		i += n2
	}
	return i, nil
}

func (m *S2Config) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *S2Config) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	if m.MinLevel != 0 {
		dAtA[i] = 0x8
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.MinLevel))
	}
	if m.MaxLevel != 0 {
		dAtA[i] = 0x10
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.MaxLevel))
	}
	if m.LevelMod != 0 {
		dAtA[i] = 0x18
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.LevelMod))
	}
	if m.MaxCells != 0 {
		dAtA[i] = 0x20
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.MaxCells))
	}
	return i, nil
}

func (m *S2GeographyConfig) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *S2GeographyConfig) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	if m.S2Config != nil {
		dAtA[i] = 0xa
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.S2Config.Size()))
		n3, err := m.S2Config.MarshalTo(dAtA[i:])
		if err != nil {
			return 0, err
		}
		i += n3
	}
	return i, nil
}

func (m *S2GeometryConfig) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *S2GeometryConfig) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	if m.MinX != 0 {
		dAtA[i] = 0x9
		i++
		encoding_binary.LittleEndian.PutUint64(dAtA[i:], uint64(math.Float64bits(float64(m.MinX))))
		i += 8
	}
	if m.MaxX != 0 {
		dAtA[i] = 0x11
		i++
		encoding_binary.LittleEndian.PutUint64(dAtA[i:], uint64(math.Float64bits(float64(m.MaxX))))
		i += 8
	}
	if m.MinY != 0 {
		dAtA[i] = 0x19
		i++
		encoding_binary.LittleEndian.PutUint64(dAtA[i:], uint64(math.Float64bits(float64(m.MinY))))
		i += 8
	}
	if m.MaxY != 0 {
		dAtA[i] = 0x21
		i++
		encoding_binary.LittleEndian.PutUint64(dAtA[i:], uint64(math.Float64bits(float64(m.MaxY))))
		i += 8
	}
	if m.S2Config != nil {
		dAtA[i] = 0x2a
		i++
		i = encodeVarintConfig(dAtA, i, uint64(m.S2Config.Size()))
		n4, err := m.S2Config.MarshalTo(dAtA[i:])
		if err != nil {
			return 0, err
		}
		i += n4
	}
	return i, nil
}

func encodeVarintConfig(dAtA []byte, offset int, v uint64) int {
	for v >= 1<<7 {
		dAtA[offset] = uint8(v&0x7f | 0x80)
		v >>= 7
		offset++
	}
	dAtA[offset] = uint8(v)
	return offset + 1
}
func (m *Config) Size() (n int) {
	if m == nil {
		return 0
	}
	var l int
	_ = l
	if m.S2Geography != nil {
		l = m.S2Geography.Size()
		n += 1 + l + sovConfig(uint64(l))
	}
	if m.S2Geometry != nil {
		l = m.S2Geometry.Size()
		n += 1 + l + sovConfig(uint64(l))
	}
	return n
}

func (m *S2Config) Size() (n int) {
	if m == nil {
		return 0
	}
	var l int
	_ = l
	if m.MinLevel != 0 {
		n += 1 + sovConfig(uint64(m.MinLevel))
	}
	if m.MaxLevel != 0 {
		n += 1 + sovConfig(uint64(m.MaxLevel))
	}
	if m.LevelMod != 0 {
		n += 1 + sovConfig(uint64(m.LevelMod))
	}
	if m.MaxCells != 0 {
		n += 1 + sovConfig(uint64(m.MaxCells))
	}
	return n
}

func (m *S2GeographyConfig) Size() (n int) {
	if m == nil {
		return 0
	}
	var l int
	_ = l
	if m.S2Config != nil {
		l = m.S2Config.Size()
		n += 1 + l + sovConfig(uint64(l))
	}
	return n
}

func (m *S2GeometryConfig) Size() (n int) {
	if m == nil {
		return 0
	}
	var l int
	_ = l
	if m.MinX != 0 {
		n += 9
	}
	if m.MaxX != 0 {
		n += 9
	}
	if m.MinY != 0 {
		n += 9
	}
	if m.MaxY != 0 {
		n += 9
	}
	if m.S2Config != nil {
		l = m.S2Config.Size()
		n += 1 + l + sovConfig(uint64(l))
	}
	return n
}

func sovConfig(x uint64) (n int) {
	for {
		n++
		x >>= 7
		if x == 0 {
			break
		}
	}
	return n
}
func sozConfig(x uint64) (n int) {
	return sovConfig(uint64((x << 1) ^ uint64((int64(x) >> 63))))
}
func (this *Config) GetValue() interface{} {
	if this.S2Geography != nil {
		return this.S2Geography
	}
	if this.S2Geometry != nil {
		return this.S2Geometry
	}
	return nil
}

func (this *Config) SetValue(value interface{}) bool {
	switch vt := value.(type) {
	case *S2GeographyConfig:
		this.S2Geography = vt
	case *S2GeometryConfig:
		this.S2Geometry = vt
	default:
		return false
	}
	return true
}
func (m *Config) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowConfig
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: Config: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: Config: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field S2Geography", wireType)
			}
			var msglen int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				msglen |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			if msglen < 0 {
				return ErrInvalidLengthConfig
			}
			postIndex := iNdEx + msglen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			if m.S2Geography == nil {
				m.S2Geography = &S2GeographyConfig{}
			}
			if err := m.S2Geography.Unmarshal(dAtA[iNdEx:postIndex]); err != nil {
				return err
			}
			iNdEx = postIndex
		case 2:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field S2Geometry", wireType)
			}
			var msglen int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				msglen |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			if msglen < 0 {
				return ErrInvalidLengthConfig
			}
			postIndex := iNdEx + msglen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			if m.S2Geometry == nil {
				m.S2Geometry = &S2GeometryConfig{}
			}
			if err := m.S2Geometry.Unmarshal(dAtA[iNdEx:postIndex]); err != nil {
				return err
			}
			iNdEx = postIndex
		default:
			iNdEx = preIndex
			skippy, err := skipConfig(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthConfig
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func (m *S2Config) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowConfig
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: S2Config: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: S2Config: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 0 {
				return fmt.Errorf("proto: wrong wireType = %d for field MinLevel", wireType)
			}
			m.MinLevel = 0
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				m.MinLevel |= (int32(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
		case 2:
			if wireType != 0 {
				return fmt.Errorf("proto: wrong wireType = %d for field MaxLevel", wireType)
			}
			m.MaxLevel = 0
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				m.MaxLevel |= (int32(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
		case 3:
			if wireType != 0 {
				return fmt.Errorf("proto: wrong wireType = %d for field LevelMod", wireType)
			}
			m.LevelMod = 0
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				m.LevelMod |= (int32(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
		case 4:
			if wireType != 0 {
				return fmt.Errorf("proto: wrong wireType = %d for field MaxCells", wireType)
			}
			m.MaxCells = 0
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				m.MaxCells |= (int32(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
		default:
			iNdEx = preIndex
			skippy, err := skipConfig(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthConfig
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func (m *S2GeographyConfig) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowConfig
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: S2GeographyConfig: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: S2GeographyConfig: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field S2Config", wireType)
			}
			var msglen int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				msglen |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			if msglen < 0 {
				return ErrInvalidLengthConfig
			}
			postIndex := iNdEx + msglen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			if m.S2Config == nil {
				m.S2Config = &S2Config{}
			}
			if err := m.S2Config.Unmarshal(dAtA[iNdEx:postIndex]); err != nil {
				return err
			}
			iNdEx = postIndex
		default:
			iNdEx = preIndex
			skippy, err := skipConfig(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthConfig
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func (m *S2GeometryConfig) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowConfig
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: S2GeometryConfig: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: S2GeometryConfig: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 1 {
				return fmt.Errorf("proto: wrong wireType = %d for field MinX", wireType)
			}
			var v uint64
			if (iNdEx + 8) > l {
				return io.ErrUnexpectedEOF
			}
			v = uint64(encoding_binary.LittleEndian.Uint64(dAtA[iNdEx:]))
			iNdEx += 8
			m.MinX = float64(math.Float64frombits(v))
		case 2:
			if wireType != 1 {
				return fmt.Errorf("proto: wrong wireType = %d for field MaxX", wireType)
			}
			var v uint64
			if (iNdEx + 8) > l {
				return io.ErrUnexpectedEOF
			}
			v = uint64(encoding_binary.LittleEndian.Uint64(dAtA[iNdEx:]))
			iNdEx += 8
			m.MaxX = float64(math.Float64frombits(v))
		case 3:
			if wireType != 1 {
				return fmt.Errorf("proto: wrong wireType = %d for field MinY", wireType)
			}
			var v uint64
			if (iNdEx + 8) > l {
				return io.ErrUnexpectedEOF
			}
			v = uint64(encoding_binary.LittleEndian.Uint64(dAtA[iNdEx:]))
			iNdEx += 8
			m.MinY = float64(math.Float64frombits(v))
		case 4:
			if wireType != 1 {
				return fmt.Errorf("proto: wrong wireType = %d for field MaxY", wireType)
			}
			var v uint64
			if (iNdEx + 8) > l {
				return io.ErrUnexpectedEOF
			}
			v = uint64(encoding_binary.LittleEndian.Uint64(dAtA[iNdEx:]))
			iNdEx += 8
			m.MaxY = float64(math.Float64frombits(v))
		case 5:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field S2Config", wireType)
			}
			var msglen int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				msglen |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			if msglen < 0 {
				return ErrInvalidLengthConfig
			}
			postIndex := iNdEx + msglen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			if m.S2Config == nil {
				m.S2Config = &S2Config{}
			}
			if err := m.S2Config.Unmarshal(dAtA[iNdEx:postIndex]); err != nil {
				return err
			}
			iNdEx = postIndex
		default:
			iNdEx = preIndex
			skippy, err := skipConfig(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthConfig
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func skipConfig(dAtA []byte) (n int, err error) {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return 0, ErrIntOverflowConfig
			}
			if iNdEx >= l {
				return 0, io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		wireType := int(wire & 0x7)
		switch wireType {
		case 0:
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return 0, ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return 0, io.ErrUnexpectedEOF
				}
				iNdEx++
				if dAtA[iNdEx-1] < 0x80 {
					break
				}
			}
			return iNdEx, nil
		case 1:
			iNdEx += 8
			return iNdEx, nil
		case 2:
			var length int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return 0, ErrIntOverflowConfig
				}
				if iNdEx >= l {
					return 0, io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				length |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			iNdEx += length
			if length < 0 {
				return 0, ErrInvalidLengthConfig
			}
			return iNdEx, nil
		case 3:
			for {
				var innerWire uint64
				var start int = iNdEx
				for shift := uint(0); ; shift += 7 {
					if shift >= 64 {
						return 0, ErrIntOverflowConfig
					}
					if iNdEx >= l {
						return 0, io.ErrUnexpectedEOF
					}
					b := dAtA[iNdEx]
					iNdEx++
					innerWire |= (uint64(b) & 0x7F) << shift
					if b < 0x80 {
						break
					}
				}
				innerWireType := int(innerWire & 0x7)
				if innerWireType == 4 {
					break
				}
				next, err := skipConfig(dAtA[start:])
				if err != nil {
					return 0, err
				}
				iNdEx = start + next
			}
			return iNdEx, nil
		case 4:
			return iNdEx, nil
		case 5:
			iNdEx += 4
			return iNdEx, nil
		default:
			return 0, fmt.Errorf("proto: illegal wireType %d", wireType)
		}
	}
	panic("unreachable")
}

var (
	ErrInvalidLengthConfig = fmt.Errorf("proto: negative length found during unmarshaling")
	ErrIntOverflowConfig   = fmt.Errorf("proto: integer overflow")
)

func init() { proto.RegisterFile("geo/geoindex/config.proto", fileDescriptor_config_4fdfa32e25381f1e) }

var fileDescriptor_config_4fdfa32e25381f1e = []byte{
	// 376 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x9c, 0x92, 0xbf, 0x6e, 0xea, 0x30,
	0x18, 0xc5, 0x63, 0x2e, 0xa0, 0x60, 0xee, 0x70, 0x6f, 0xee, 0x55, 0x95, 0xb6, 0x92, 0x41, 0x4c,
	0xb4, 0x43, 0x90, 0xd2, 0x0d, 0xa9, 0x4b, 0x19, 0xaa, 0x4a, 0x74, 0x81, 0x05, 0xba, 0x44, 0x69,
	0x70, 0x4d, 0xd4, 0x24, 0x46, 0x09, 0xaa, 0x9c, 0xbd, 0x0f, 0xd0, 0x47, 0x60, 0xe7, 0x45, 0x18,
	0x19, 0x19, 0xdb, 0xb0, 0xf4, 0x31, 0xaa, 0x7c, 0x76, 0xa8, 0xfa, 0x77, 0xe8, 0x66, 0x7f, 0xe7,
	0x7c, 0x3f, 0x9d, 0xe3, 0x04, 0xef, 0x33, 0xca, 0x3b, 0x8c, 0x72, 0x3f, 0x9a, 0x50, 0xd1, 0xf1,
	0x78, 0x74, 0xe3, 0x33, 0x6b, 0x16, 0xf3, 0x39, 0x37, 0xf6, 0x3c, 0xee, 0xdd, 0xc6, 0xdc, 0xf5,
	0xa6, 0x16, 0xa3, 0xdc, 0x2a, 0x4c, 0x07, 0xff, 0x19, 0x67, 0x1c, 0x2c, 0x9d, 0xfc, 0x24, 0xdd,
	0xad, 0x25, 0xc2, 0xd5, 0x1e, 0xac, 0x1b, 0x7d, 0xfc, 0x3b, 0xb1, 0x1d, 0x46, 0x39, 0x8b, 0xdd,
	0xd9, 0x34, 0x35, 0x51, 0x13, 0xb5, 0xeb, 0xf6, 0x91, 0xf5, 0x39, 0xcf, 0x1a, 0xda, 0xe7, 0x85,
	0x55, 0x02, 0x06, 0xf5, 0xe4, 0x75, 0x64, 0x5c, 0xe0, 0xba, 0xa4, 0x85, 0x74, 0x1e, 0xa7, 0x66,
	0x09, 0x60, 0xed, 0x6f, 0x61, 0xe0, 0x54, 0x2c, 0x9c, 0xec, 0x26, 0x5d, 0x7d, 0xb5, 0x68, 0xa0,
	0xe7, 0x45, 0x03, 0xb5, 0xee, 0x11, 0xd6, 0x87, 0xb6, 0xca, 0x7b, 0x88, 0x6b, 0xa1, 0x1f, 0x39,
	0x01, 0xbd, 0xa3, 0x01, 0x84, 0xad, 0x0c, 0xf4, 0xd0, 0x8f, 0xfa, 0xf9, 0x1d, 0x44, 0x57, 0x28,
	0xb1, 0xa4, 0x44, 0x57, 0xec, 0x44, 0x10, 0x9c, 0x90, 0x4f, 0xcc, 0x5f, 0x52, 0x84, 0xc1, 0x25,
	0x9f, 0x14, 0x9b, 0x1e, 0x0d, 0x82, 0xc4, 0x2c, 0xef, 0x36, 0x7b, 0xf9, 0xbd, 0x5b, 0x86, 0x18,
	0x23, 0xfc, 0xf7, 0x43, 0x7b, 0xe3, 0x14, 0xd7, 0x12, 0xdb, 0x91, 0x9f, 0x42, 0xbd, 0x5d, 0xf3,
	0xeb, 0xba, 0xaa, 0xa6, 0x9e, 0xa8, 0x93, 0x22, 0x2f, 0x11, 0xfe, 0xf3, 0xfe, 0x2d, 0x8c, 0x7f,
	0xb8, 0x92, 0x17, 0x15, 0x40, 0x45, 0x83, 0x72, 0xe8, 0x47, 0x23, 0x18, 0xba, 0xc2, 0x11, 0x50,
	0x2e, 0x1f, 0xba, 0x62, 0x54, 0x38, 0x53, 0x28, 0x25, 0x9d, 0xe3, 0xc2, 0x99, 0x42, 0x19, 0xe9,
	0x1c, 0xbf, 0x4d, 0x5b, 0xf9, 0x59, 0xda, 0xb3, 0xe3, 0xd5, 0x13, 0xd1, 0x56, 0x19, 0x41, 0xeb,
	0x8c, 0xa0, 0x4d, 0x46, 0xd0, 0x63, 0x46, 0xd0, 0xc3, 0x96, 0x68, 0xeb, 0x2d, 0xd1, 0x36, 0x5b,
	0xa2, 0x5d, 0xe9, 0x05, 0xe4, 0xba, 0x0a, 0xff, 0xdb, 0xc9, 0x4b, 0x00, 0x00, 0x00, 0xff, 0xff,
	0xb1, 0xfa, 0x92, 0x6c, 0xba, 0x02, 0x00, 0x00,
}
