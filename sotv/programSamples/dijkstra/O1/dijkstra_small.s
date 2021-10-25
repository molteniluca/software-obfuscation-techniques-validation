	.file	"dijkstra_small.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	" %d"
	.text
	.globl	print_path
	.type	print_path, @function
print_path:
.LFB23:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	%esi, %ebx
	movslq	%esi, %rax
	movl	4(%rdi,%rax,8), %esi
	cmpl	$9999, %esi
	je	.L2
	call	print_path
.L2:
	movl	%ebx, %edx
	movl	$.LC0, %esi
	movl	$1, %edi
	movl	$0, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE23:
	.size	print_path, .-print_path
	.section	.rodata.str1.1
.LC1:
	.string	"Out of memory.\n"
	.text
	.globl	enqueue
	.type	enqueue, @function
enqueue:
.LFB24:
	.cfi_startproc
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	movl	%edi, %r12d
	movl	%esi, %ebp
	movl	%edx, %ebx
	movl	$24, %edi
	call	malloc
	movq	qHead(%rip), %rcx
	testq	%rax, %rax
	jne	.L5
	movq	stderr(%rip), %rcx
	movl	$15, %edx
	movl	$1, %esi
	movl	$.LC1, %edi
	call	fwrite
	movl	$1, %edi
	call	exit
.L5:
	movl	%r12d, (%rax)
	movl	%ebp, 4(%rax)
	movl	%ebx, 8(%rax)
	movq	$0, 16(%rax)
	testq	%rcx, %rcx
	jne	.L9
	movq	%rax, qHead(%rip)
	jmp	.L7
.L8:
	movq	%rdx, %rcx
.L9:
	movq	16(%rcx), %rdx
	testq	%rdx, %rdx
	jne	.L8
	movq	%rax, 16(%rcx)
.L7:
	addl	$1, g_qCount(%rip)
	popq	%rbx
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE24:
	.size	enqueue, .-enqueue
	.globl	dequeue
	.type	dequeue, @function
dequeue:
.LFB25:
	.cfi_startproc
	movq	qHead(%rip), %rax
	testq	%rax, %rax
	je	.L15
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	movl	(%rax), %ecx
	movl	%ecx, (%rdi)
	movq	qHead(%rip), %rcx
	movl	4(%rcx), %ecx
	movl	%ecx, (%rsi)
	movq	qHead(%rip), %rcx
	movl	8(%rcx), %ecx
	movl	%ecx, (%rdx)
	movq	qHead(%rip), %rdx
	movq	16(%rdx), %rdx
	movq	%rdx, qHead(%rip)
	movq	%rax, %rdi
	call	free
	subl	$1, g_qCount(%rip)
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
.L15:
	rep ret
	.cfi_endproc
.LFE25:
	.size	dequeue, .-dequeue
	.globl	qcount
	.type	qcount, @function
qcount:
.LFB26:
	.cfi_startproc
	movl	g_qCount(%rip), %eax
	ret
	.cfi_endproc
.LFE26:
	.size	qcount, .-qcount
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC2:
	.string	"Shortest path is 0 in cost. Just stay where you are."
	.section	.rodata.str1.1
.LC3:
	.string	"Shortest path is %d in cost. "
.LC4:
	.string	"Path is: "
	.text
	.globl	dijkstra
	.type	dijkstra, @function
dijkstra:
.LFB27:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	%esi, %ebx
	movl	$rgnNodes, %eax
	movl	$rgnNodes+800, %edx
.L18:
	movl	$9999, (%rax)
	movl	$9999, 4(%rax)
	addq	$8, %rax
	cmpq	%rax, %rdx
	jne	.L18
	movl	$100, ch(%rip)
	cmpl	%ebx, %edi
	jne	.L19
	movl	$.LC2, %edi
	call	puts
	jmp	.L20
.L19:
	movslq	%edi, %rax
	movl	$0, rgnNodes(,%rax,8)
	movl	$9999, rgnNodes+4(,%rax,8)
	movl	$9999, %edx
	movl	$0, %esi
	call	enqueue
	jmp	.L21
.L25:
	movl	$iPrev, %edx
	movl	$iDist, %esi
	movl	$iNode, %edi
	call	dequeue
	movl	$0, i(%rip)
	movl	$0, %edi
.L24:
	movl	iNode(%rip), %edx
	movslq	%edi, %rax
	movslq	%edx, %rcx
	leaq	(%rcx,%rcx,4), %rcx
	leaq	(%rcx,%rcx,4), %rcx
	leaq	(%rax,%rcx,4), %rax
	movl	AdjMatrix(,%rax,4), %esi
	movl	%esi, iCost(%rip)
	cmpl	$9999, %esi
	je	.L22
	movslq	%edi, %rax
	movl	rgnNodes(,%rax,8), %eax
	cmpl	$9999, %eax
	je	.L23
	movl	%esi, %ecx
	addl	iDist(%rip), %ecx
	cmpl	%ecx, %eax
	jle	.L22
.L23:
	addl	iDist(%rip), %esi
	movslq	%edi, %rax
	movl	%esi, rgnNodes(,%rax,8)
	movl	%edx, rgnNodes+4(,%rax,8)
	call	enqueue
.L22:
	movl	i(%rip), %eax
	leal	1(%rax), %edi
	movl	%edi, i(%rip)
	cmpl	$99, %edi
	jle	.L24
.L21:
	cmpl	$0, g_qCount(%rip)
	jg	.L25
	movslq	%ebx, %rax
	movl	rgnNodes(,%rax,8), %edx
	movl	$.LC3, %esi
	movl	$1, %edi
	movl	$0, %eax
	call	__printf_chk
	movl	$.LC4, %esi
	movl	$1, %edi
	movl	$0, %eax
	call	__printf_chk
	movl	%ebx, %esi
	movl	$rgnNodes, %edi
	call	print_path
	movl	$10, %edi
	call	putchar
.L20:
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE27:
	.size	dijkstra, .-dijkstra
	.section	.rodata.str1.1
.LC5:
	.string	"r"
.LC6:
	.string	"input.dat"
.LC7:
	.string	"%d"
	.text
	.globl	main
	.type	main, @function
main:
.LFB28:
	.cfi_startproc
	pushq	%r13
	.cfi_def_cfa_offset 16
	.cfi_offset 13, -16
	pushq	%r12
	.cfi_def_cfa_offset 24
	.cfi_offset 12, -24
	pushq	%rbp
	.cfi_def_cfa_offset 32
	.cfi_offset 6, -32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	subq	$24, %rsp
	.cfi_def_cfa_offset 64
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	movl	$.LC5, %esi
	movl	$.LC6, %edi
	call	fopen
	movq	%rax, %r12
	movl	$AdjMatrix, %ebx
	movl	$AdjMatrix+40000, %r13d
	jmp	.L30
.L31:
	leaq	4(%rsp), %rdx
	movl	$.LC7, %esi
	movq	%r12, %rdi
	movl	$0, %eax
	call	__isoc99_fscanf
	movl	4(%rsp), %eax
	movl	%eax, (%rbx)
	addq	$4, %rbx
	cmpq	%rbp, %rbx
	jne	.L31
	movq	%rbp, %rbx
	cmpq	%rbp, %r13
	je	.L34
.L30:
	leaq	400(%rbx), %rbp
	jmp	.L31
.L34:
	movl	$50, %ecx
	movl	$0, %ebp
	movl	$1374389535, %r12d
.L32:
	movl	%ecx, %eax
	imull	%r12d
	sarl	$5, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	imull	$100, %edx, %ebx
	subl	%ebx, %ecx
	movl	%ecx, %ebx
	movl	%ecx, %esi
	movl	%ebp, %edi
	call	dijkstra
	addl	$1, %ebp
	leal	1(%rbx), %ecx
	cmpl	$20, %ebp
	jne	.L32
	movl	$0, %edi
	call	exit
	.cfi_endproc
.LFE28:
	.size	main, .-main
	.comm	iDist,4,4
	.comm	iCost,4,4
	.comm	i,4,4
	.comm	iNode,4,4
	.comm	iPrev,4,4
	.comm	ch,4,4
	.comm	rgnNodes,800,32
	.globl	g_qCount
	.bss
	.align 4
	.type	g_qCount, @object
	.size	g_qCount, 4
g_qCount:
	.zero	4
	.comm	AdjMatrix,40000,32
	.globl	qHead
	.align 8
	.type	qHead, @object
	.size	qHead, 8
qHead:
	.zero	8
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
