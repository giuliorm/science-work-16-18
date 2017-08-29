#using System;
#using System.Collections.Generic;
#using System.Linq;
#using System.Text;
#using System.Threading.Tasks;
#using System.IO;
#using System.Runtime.Serialization.Formatters;
#using System.Runtime.Serialization.Formatters.Binary;
#using SharpDX;
#using Fusion;
#using Fusion.Core.Mathematics;
#using Fusion.Drivers.Graphics;
#using Fusion.Core;
#using Fusion.Core.Content;


#namespace Fusion.Engine.Graphics {
class Scene:
	def __init__(self):
		self.nodes = [] 	#List<Node>			nodes		= new List<Node>();
		self.meshes = []  	#List<Mesh>			meshes		= new List<Mesh>();
		self.materials = [] #List<MaterialRef>	materials	= new List<MaterialRef>();
		self.firstFrame = 0
		self.lastFrame = 0
		self.trackCount = 0
		self.animData = None#Matrix[,]	animData = null;

		#protected override void Dispose ( bool disposing )
		#{
		#	if (disposing) {
		#			foreach ( var mesh in Meshes ) {
		#			if (mesh!=null) {
		#				mesh.Dispose();
		#			}
		#		}
		#	}
		#	base.Dispose(disposing);
		#}


		#/*---------------------------------------------------------------------
		# *
		# *	Topology stuff :
		# *
		---------------------------------------------------------------------*/

		#/// <summary>
		#/// Copies absolute transform to provided array.
		#/// </summary>
		#/// <param name="destination"></param>
		#public void CopyLocalTransformsTo ( Matrix[] destination )
		#{
	def CopyLocalTransformsTo(self, destination):
		for i in xrange(len(self.nodes)):
			node = self.nodes[i]
			transform = node.Transform
			destination[i] = transform

	#	@	/// <summary>
	#	/// Copies absolute transform to provided array.
	#	/// </summary>
	#	/// <param name="destination"></param>
	#public void ComputeAbsoluteTransforms ( Matrix[] destination )
	def  ComputeAbsoluteTransforms(self, destination):
	#{
		if  len(destination) < len(self.nodes):
			return
		#{
		#	throw new ArgumentOutOfRangeException("destination.Length must be greater of equal to Nodes.Count");
		#}


		#if false
		for i in xrange(len(self.nodes)):
			node = self.nodes[i]
			transform = node.Transform
			parentIndex = node.ParentIndex

			transform.Transpose()

			while parentIndex!=-1:
				parent = self.nodes[parentIndex].Transform
				parent.Transpose()
				transform = parent * transform
				parentIndex = self.nodes[parentIndex].ParentIndex

			transform.Transpose()
			destination[i] = transform

		#else
		for  i in xrange(len(self.nodes)):
			node = self.nodes[i]
			transform = node.Transform
			parentIndex = node.ParentIndex

			while parentIndex!=-1:
				parent = self.nodes[parentIndex].Transform
				transform =	transform * parent
				parentIndex = self.nodes[parentIndex].ParentIndex
			destination[i] = transform

		#/// <summary>
		#/// Computes absolute transformations using local transforms and scene's hierarchy.
		#/// Number of source matricies, destination matricies and node count must be equal.
		#/// Arguments 'sourceLocalTransforms' and 'destinationGlobalTransforms' may be the same object.
		#/// </summary>
		#/// <param name="sourceLocalTransforms"></param>
		#/// <param name="destinationGlobalTransforms"></param>
		#public void ComputeAbsoluteTransforms ( Matrix[] source, Matrix[] destination )
	def ComputeAbsoluteTransforms2(self, source, destination):
	#{
		if  source is None or destination is None or len(source) < len(self.nodes) or len(destination) < \
				len(self.nodes):
			return

		for i in xrange(len(self.nodes)):

			node = self.nodes[i]
			transform = source[i]
			parentIndex = node.ParentIndex

			while parentIndex!=-1:
				transform =	transform * source[parentIndex]
				parentIndex =	self.nodes[parentIndex].ParentIndex
			destination[i] = transform

		#/// <summary>
		#/// Computes bones transforms for skinning taking in account bind position.
		#/// </summary>
		#/// <param name="source">Local bone transforms</param>
		#/// <param name="destination">Global bone transforms multiplied by bind pose matrix</param>
	#public void ComputeBoneTransforms ( Matrix[] source, Matrix[] destination )
	#{
	def ComputeBoneTransforms(self, source, destination):
		self.ComputeAbsoluteTransforms2(source, destination)
		for i in xrange(len(self.nodes)):
			destination[i] = Matrix.Invert( Nodes[i].BindPose ) * destination[i];
		}
	}

		/*-----------------------------------------------------------------------------------------
		 *
		 *	Animation stuff :
		 *
		-----------------------------------------------------------------------------------------*/

		/// <summary>
		/// Deletes all animation data.
		/// </summary>
		public void DeleteAnimation ()
		{
			animData		=	null;
			firstFrame		=	0;
			lastFrame		=	0;
			trackCount	=	0;
		}



		/// <summary>
		/// Creates animation data
		/// </summary>
		/// <param name="firstFrame">Inclusive first frame</param>
		/// <param name="lastFrame"></param>
		/// <param name="nodeCount"></param>
		public void CreateAnimation ( int firstFrame, int lastFrame, int nodeCount )
		{
			if ( firstFrame > lastFrame ) {
				throw new ArgumentException("firstFrame > lastFrame");
			}
			if ( nodeCount <= 0 ) {
				throw new ArgumentException("nodeCount must be positive");
			}

			this.firstFrame		=	firstFrame;
			this.lastFrame		=	lastFrame;
			this.trackCount	=	nodeCount;

			animData	=	new Matrix[ lastFrame - firstFrame + 1, nodeCount ];
		}



		/// <summary>
		/// Sets animation key
		/// </summary>
		/// <param name="frame"></param>
		/// <param name="nodeIndex"></param>
		/// <param name="transform"></param>
		public void SetAnimKey ( int frame, int trackIndex, Matrix transform )
		{
			if ( animData==null ) {
				throw new InvalidOperationException("Animation data is not created");
			}
			if ( frame < firstFrame	|| frame > lastFrame ) {
				throw new ArgumentOutOfRangeException("frame");
			}
			if ( trackIndex < 0	|| trackIndex >= trackCount ) {
				throw new ArgumentOutOfRangeException("trackIndex");
			}

			animData[ frame - firstFrame, trackIndex ] = transform;
		}



		/// <summary>
		/// Gets animation key
		/// </summary>
		/// <param name="frame"></param>
		/// <param name="nodeId"></param>
		/// <returns></returns>
		public Matrix GetAnimKey ( int frame, int trackIndex )
		{
			if ( animData==null ) {
				throw new InvalidOperationException("Animation data is not created");
			}
			if ( frame < firstFrame	|| frame > lastFrame ) {
				throw new ArgumentOutOfRangeException("frame");
			}
			if ( trackIndex < 0	|| trackIndex >= trackCount ) {
				throw new ArgumentOutOfRangeException("trackIndex");
			}

			return animData[ frame - firstFrame, trackIndex ];
		}



		/// <summary>
		/// Get local matricies for each node for given animation frame.
		/// First, this method copies node's local matricies
		/// then, it replace this matrices by node's animation track values.
		/// </summary>
		/// <param name="frame"></param>
		/// <returns></returns>
		public void GetAnimSnapshot ( int frame, Matrix[] destination )
		{
			if ( animData==null ) {
				throw new InvalidOperationException("Animation data is not created");
			}

			if (destination.Length<Nodes.Count) {
				throw new ArgumentException("destination.Length must be greater of equal to Nodes.Count");
			}

			for (int i=0; i<Nodes.Count; i++) {
				var node = Nodes[i];
				destination[i] = node.TrackIndex < 0 ? node.Transform : GetAnimKey( frame, node.TrackIndex );
			}
		}


		/// <summary>
		/// Get local matricies for each node for given animation frame.
		/// First, this method copies node's local matricies
		/// then, it replace this matrices by node's animation track values.
		/// </summary>
		/// <param name="frame"></param>
		/// <returns></returns>
		public void GetAnimSnapshot ( float frame, int firstFrame, int lastFrame, AnimationMode animMode, Matrix[] destination )
		{
			if ( animData==null ) {
				throw new InvalidOperationException("Animation data is not created");
			}

			if (destination.Length<Nodes.Count) {
				throw new ArgumentOutOfRangeException("destination.Length must be greater of equal to Nodes.Count");
			}

			if ( firstFrame < FirstFrame || firstFrame > LastFrame ) {
				throw new ArgumentOutOfRangeException("firstFrame");
			}
			if ( lastFrame < FirstFrame || lastFrame > LastFrame ) {
				throw new ArgumentOutOfRangeException("firstFrame");
			}
			if ( firstFrame > lastFrame ) {
				throw new ArgumentOutOfRangeException("firstFrame > lastFrame");
			}


			int frame0	=	(int)Math.Floor( frame );
			int frame1	=	frame0 + 1;
			var factor	=	(frame > 0) ? (frame%1) : (1 + frame%1);

			if (animMode==AnimationMode.Repeat) {
				frame0	=	MathUtil.Wrap( frame0, firstFrame, lastFrame );
				frame1	=	MathUtil.Wrap( frame1, firstFrame, lastFrame );
			} else if (animMode==AnimationMode.Clamp) {
				frame0	=	MathUtil.Clamp( frame0, firstFrame, lastFrame );
				frame1	=	MathUtil.Clamp( frame1, firstFrame, lastFrame );
			}

			for (int i=0; i<Nodes.Count; i++) {
				var node = Nodes[i];

				if (node.TrackIndex<0) {
					destination[i] = node.Transform;
				} else {

					var x0	=	GetAnimKey( frame0, node.TrackIndex );
					var x1	=	GetAnimKey( frame1, node.TrackIndex );

					Quaternion q0, q1;
					Vector3 t0, t1;
					Vector3 s0, s1;

					x0.Decompose( out s0, out q0, out t0 );
					x1.Decompose( out s1, out q1, out t1 );

					var q	=	Quaternion.Slerp( q0, q1, factor );
					var t	=	Vector3.Lerp( t0, t1, factor );
					var s	=	Vector3.Lerp( s0, s1, factor );

					var x	=	Matrix.Scaling( s ) * Matrix.RotationQuaternion( q ) * Matrix.Translation( t );

					destination[i] = x;
				}
			}
		}

		/*-----------------------------------------------------------------------------------------
		 *
		 *	Optimization stuff :
		 *
		-----------------------------------------------------------------------------------------*/

		class Comparer : IEqualityComparer<Mesh> {
			public bool Equals ( Mesh a, Mesh b )
			{
				return a.Equals(b);
			}

			public int GetHashCode ( Mesh a ) {
				return a.GetHashCode();
			}
		}

		/// <summary>
		///
		/// </summary>
		public void DetectAndMergeInstances ()
		{
			//	creates groups of each mesh :
			var nodeMeshGroups	=	Nodes
									.Where( n1 => n1.MeshIndex >= 0 )
									.Select( n2 => new { Node = n2, Mesh = Meshes[n2.MeshIndex] } )
									.GroupBy( nm => nm.Mesh, nm => nm.Node )
									.ToArray();

			//foreach ( var ig in nodeMeshGroups ) {
			//	Log.Message("{0}", ig.Key.ToString());
			//	foreach ( var n in ig ) {
			//		Log.Message("  {0}", n.Name );
			//	}
			//}

			meshes	=	nodeMeshGroups
						.Select( nmg => nmg.Key )
						.ToList();

			for	( int i=0; i<nodeMeshGroups.Length; i++) {
				foreach ( var n in nodeMeshGroups[i] ) {
					n.MeshIndex = i;
				}
			}
		}

		/*-----------------------------------------------------------------------------------------
		 *
		 *	Save/Load stuff :
		 *
		-----------------------------------------------------------------------------------------*/

		/// <summary>
		/// Loads scene
		/// </summary>
		/// <param name="path"></param>
		/// <returns></returns>
		public static Scene Load( Stream stream )
		{
			var scene = new Scene();

			using( var reader = new BinaryReader( stream ) ) {

				reader.ExpectFourCC("SCN1", "scene");

				//---------------------------------------------
				scene.StartTime		=	new TimeSpan( reader.ReadInt64() );
				scene.EndTime		=	new TimeSpan( reader.ReadInt64() );
				scene.firstFrame	=	reader.ReadInt32();
				scene.lastFrame		=	reader.ReadInt32();
				scene.trackCount	=	reader.ReadInt32();

				reader.ExpectFourCC("ANIM", "scene");

				if (scene.trackCount!=0) {
					scene.CreateAnimation( scene.FirstFrame, scene.LastFrame, scene.trackCount );
				}

				for (int fi=scene.firstFrame; fi<=scene.lastFrame; fi++) {
					for (int ni=0; ni<scene.trackCount; ni++) {
						scene.animData[ fi - scene.firstFrame, ni ] = reader.Read<Matrix>();
					}
				}

				//---------------------------------------------
				reader.ExpectFourCC("MTRL", "scene");

				var mtrlCount = reader.ReadInt32();

				scene.materials.Clear();

				for ( int i=0; i<mtrlCount; i++) {
					var mtrl	=	new MaterialRef();
					mtrl.Name	=	reader.ReadString();

					if (reader.ReadBoolean()==true) {
						mtrl.Texture = reader.ReadString();
					} else {
						mtrl.Texture = null;
					}
					scene.Materials.Add( mtrl );
				}

				//---------------------------------------------
				reader.ExpectFourCC("NODE", "scene");

				var nodeCount = reader.ReadInt32();

				for ( int i = 0; i < nodeCount; ++i ) {
					var node = new Node();
					node.Name			=	reader.ReadString();
					node.ParentIndex	=	reader.ReadInt32();
					node.MeshIndex		=	reader.ReadInt32();
					node.TrackIndex		=	reader.ReadInt32();
					node.Transform		=	reader.Read<Matrix>();
					node.BindPose		=	reader.Read<Matrix>();
					scene.nodes.Add( node );
				}

				//---------------------------------------------
				reader.ExpectFourCC("MESH", "scene");

				var meshCount = reader.ReadInt32();

				for ( int i = 0; i < meshCount; i++ ) {
					var mesh = new Mesh();
					mesh.Deserialize( reader );
					scene.Meshes.Add( mesh );
				}
			}

			return scene;
		}



		/// <summary>
		/// Saves scene
		/// </summary>
		/// <param name="path"></param>
		public void Save( Stream stream ) {

			using( var writer = new BinaryWriter( stream ) ) {

				//---------------------------------------------
				writer.Write(new[]{'S','C','N','1'});

				writer.Write( StartTime.Ticks );
				writer.Write( EndTime.Ticks );
				writer.Write( FirstFrame );
				writer.Write( LastFrame	);
				writer.Write( trackCount );

				//---------------------------------------------
				writer.Write(new[]{'A','N','I','M'});

				for (int fi=firstFrame; fi<=lastFrame; fi++) {
					for (int ni=0; ni<trackCount; ni++) {
						writer.Write( animData[ fi - firstFrame, ni ] );
					}
				}

				//---------------------------------------------
				writer.Write(new[]{'M','T','R','L'});

				writer.Write( Materials.Count );

				foreach ( var mtrl in Materials ) {
					writer.Write( mtrl.Name );
					if ( mtrl.Texture!=null ) {
						writer.Write( true );
						writer.Write( mtrl.Texture );
					} else {
						writer.Write( false );
					}
				}

				//---------------------------------------------
				writer.Write(new[]{'N','O','D','E'});

				writer.Write( Nodes.Count );

				foreach ( var node in Nodes ) {
					writer.Write( node.Name );
					writer.Write( node.ParentIndex );
					writer.Write( node.MeshIndex );
					writer.Write( node.TrackIndex );
					writer.Write( node.Transform );
					writer.Write( node.BindPose );
				}

				//---------------------------------------------
				writer.Write(new[]{'M','E','S','H'});

				writer.Write( Meshes.Count );

				foreach ( var mesh in Meshes ) {
					mesh.Serialize( writer );
				}
			}
		}



		/// <summary>
		/// Make texture paths relative to base directory.
		/// </summary>
		/// <param name="sceneFullPath"></param>
		/// <param name="baseDirectory"></param>
		public void ResolveTexturePathToBaseDirectory ( string sceneFullPath, string baseDirectory )
		{
			Log.Message("{0}", baseDirectory);
			var baseDirUri			= new Uri( baseDirectory + @"\" );
			var sceneDirFullPath	= Path.GetDirectoryName( Path.GetFullPath( sceneFullPath ) ) + @"\";

			Log.Message("{0}", baseDirUri );

			foreach ( var mtrl in Materials ) {

				if (mtrl.Texture==null) {
					continue;
				}
				Log.Message( "-" + mtrl.Texture );

				var absTexPath		=	Path.Combine( sceneDirFullPath, mtrl.Texture );
				var texUri			=	new Uri( absTexPath );
				mtrl.Texture	=	baseDirUri.MakeRelativeUri( texUri ).ToString();

				Log.Message( "-" + texUri );
				Log.Message( "+" + mtrl.Texture );
			}
		}



		public int CalculateNodeDepth ( Node node )
		{
			int depth = 0;
			while (node.ParentIndex>=0) {
				node = Nodes[node.ParentIndex];
				depth++;
			}
			return depth;
		}
	}
}