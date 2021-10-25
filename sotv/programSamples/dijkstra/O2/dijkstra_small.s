	.file	"dijkstra_small.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	" %d"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	print_path
	.type	print_path, @function
print_path:
.LFB23:
	.cfi_startproc
	movslq	%esi, %rax
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	4(%rdi,%rax,8), %esi
	movq	%rax, %rbx
	cmpl	$9999, %esi
	je	.L2
	call	print_path
.L2:
	movl	%ebx, %edx
	movl	$1, %edi
	movl	$.LC0, %esi
	xorl	%eax, %eax
	call	__printf_chk
	popq	%rbx
	.cfi_def_cfa_offset 8
	movq	stdout(%rip), %rdi
	jmp	fflush
	.cfi_endproc
.LFE23:
	.size	print_path, .-print_path
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.rodata.str1.1
.LC2:
	.string	"Out of memory.\n"
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
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
	movl	%edi, %r12d
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	movl	$24, %edi
	movl	%esi, %ebp
	movl	%edx, %ebx
	call	malloc
	testq	%rax, %rax
	movq	qHead(%rip), %rcx
	je	.L16
	testq	%rcx, %rcx
	movl	%r12d, (%rax)
	movl	%ebp, 4(%rax)
	movl	%ebx, 8(%rax)
	movq	$0, 16(%rax)
	jne	.L14
	jmp	.L17
	.p2align 4,,10
	.p2align 3
.L13:
	movq	%rdx, %rcx
.L14:
	movq	16(%rcx), %rdx
	testq	%rdx, %rdx
	jne	.L13
	movq	%rax, 16(%rcx)
	addl	$1, g_qCount(%rip)
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L17:
	.cfi_restore_state
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	movq	%rax, qHead(%rip)
	addl	$1, g_qCount(%rip)
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
.L16:
	.cfi_restore_state
	movq	stderr(%rip), %rcx
	movl	$.LC2, %edi
	movl	$15, %edx
	movl	$1, %esi
	call	fwrite
	movl	$1, %edi
	call	exit
	.cfi_endproc
.LFE24:
	.size	enqueue, .-enqueue
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.unlikely
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4,,15
	.globl	dequeue
	.type	dequeue, @function
dequeue:
.LFB25:
	.cfi_startproc
	movq	qHead(%rip), %rax
	testq	%rax, %rax
	je	.L25
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	movl	(%rax), %ecx
	movl	%ecx, (%rdi)
	movl	4(%rax), %ecx
	movq	%rax, %rdi
	movl	%ecx, (%rsi)
	movl	8(%rax), %ecx
	movl	%ecx, (%rdx)
	movq	16(%rax), %rdx
	movq	%rdx, qHead(%rip)
	call	free
	subl	$1, g_qCount(%rip)
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
.L25:
	rep ret
	.cfi_endproc
.LFE25:
	.size	dequeue, .-dequeue
	.section	.text.unlikely
.LCOLDE4:
	.text
.LHOTE4:
	.section	.text.unlikely
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4,,15
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
	.section	.text.unlikely
.LCOLDE5:
	.text
.LHOTE5:
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC6:
	.string	"Shortest path is 0 in cost. Just stay where you are."
	.section	.rodata.str1.1
.LC7:
	.string	"Shortest path is %d in cost. "
.LC8:
	.string	"Path is: "
	.section	.text.unlikely
.LCOLDB9:
	.text
.LHOTB9:
	.p2align 4,,15
	.globl	dijkstra
	.type	dijkstra, @function
dijkstra:
.LFB27:
	.cfi_startproc
	movl	$rgnNodes, %eax
	.p2align 4,,10
	.p2align 3
.L28:
	movl	$9999, (%rax)
	movl	$9999, 4(%rax)
	addq	$8, %rax
	cmpq	$rgnNodes+800, %rax
	jne	.L28
	cmpl	%esi, %edi
	movl	$100, ch(%rip)
	je	.L42
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movslq	%edi, %rax
	movl	%esi, %ebx
	movl	$9999, %edx
	xorl	%esi, %esi
	movl	$0, rgnNodes(,%rax,8)
	movl	$9999, rgnNodes+4(,%rax,8)
	call	enqueue
	movl	g_qCount(%rip), %eax
	testl	%eax, %eax
	jle	.L43
	.p2align 4,,10
	.p2align 3
.L35:
	movl	$iNode, %edi
	movl	$iPrev, %edx
	movl	$iDist, %esi
	call	dequeue
	movl	$0, i(%rip)
	xorl	%edi, %edi
	.p2align 4,,10
	.p2align 3
.L34:
	movslq	iNode(%rip), %rcx
	movslq	%edi, %rax
	movq	%rcx, %rdx
	leaq	(%rcx,%rcx,4), %rcx
	leaq	(%rcx,%rcx,4), %rcx
	leaq	(%rax,%rcx,4), %rcx
	movl	AdjMatrix(,%rcx,4), %esi
	cmpl	$9999, %esi
	movl	%esi, iCost(%rip)
	je	.L31
	movl	rgnNodes(,%rax,8), %ecx
	addl	iDist(%rip), %esi
	cmpl	$9999, %ecx
	je	.L33
	cmpl	%esi, %ecx
	jle	.L31
.L33:
	movl	%esi, rgnNodes(,%rax,8)
	movl	%edx, rgnNodes+4(,%rax,8)
	call	enqueue
.L31:
	movl	i(%rip), %eax
	leal	1(%rax), %edi
	cmpl	$99, %edi
	movl	%edi, i(%rip)
	jle	.L34
	movl	g_qCount(%rip), %eax
	testl	%eax, %eax
	jg	.L35
.L43:
	movslq	%ebx, %rax
	movl	$.LC7, %esi
	movl	$1, %edi
	movl	rgnNodes(,%rax,8), %edx
	xorl	%eax, %eax
	call	__printf_chk
	movl	$.LC8, %esi
	movl	$1, %edi
	xorl	%eax, %eax
	call	__printf_chk
	movl	%ebx, %esi
	movl	$rgnNodes, %edi
	call	print_path
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 8
	movl	$10, %edi
	jmp	putchar
.L42:
	movl	$.LC6, %edi
	jmp	puts
	.cfi_endproc
.LFE27:
	.size	dijkstra, .-dijkstra
	.section	.text.unlikely
.LCOLDE9:
	.text
.LHOTE9:
	.section	.rodata.str1.1
.LC10:
	.string	"r"
.LC11:
	.string	"input.dat"
.LC12:
	.string	"%d"
	.section	.text.unlikely
.LCOLDB13:
	.section	.text.startup,"ax",@progbits
.LHOTB13:
	.p2align 4,,15
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
	movl	$.LC10, %esi
	pushq	%rbp
	.cfi_def_cfa_offset 32
	.cfi_offset 6, -32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	movl	$.LC11, %edi
	movl	$AdjMatrix, %ebx
	movl	$AdjMatrix+40000, %r13d
	subq	$24, %rsp
	.cfi_def_cfa_offset 64
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	call	fopen
	movq	%rax, %r12
	.p2align 4,,10
	.p2align 3
.L45:
	leaq	400(%rbx), %rbp
	.p2align 4,,10
	.p2align 3
.L46:
	leaq	4(%rsp), %rdx
	xorl	%eax, %eax
	movl	$.LC12, %esi
	movq	%r12, %rdi
	addq	$4, %rbx
	call	__isoc99_fscanf
	movl	4(%rsp), %eax
	movl	%eax, -4(%rbx)
	cmpq	%rbp, %rbx
	jne	.L46
	cmpq	%rbx, %r13
	jne	.L45
	movl	$50, %ecx
	xorl	%ebp, %ebp
	movl	$1374389535, %r12d
.L48:
	movl	%ecx, %eax
	movl	%ebp, %edi
	addl	$1, %ebp
	imull	%r12d
	movl	%ecx, %eax
	sarl	$31, %eax
	sarl	$5, %edx
	subl	%eax, %edx
	imull	$100, %edx, %ebx
	subl	%ebx, %ecx
	movl	%ecx, %esi
	movl	%ecx, %ebx
	call	dijkstra
	cmpl	$20, %ebp
	leal	1(%rbx), %ecx
	jne	.L48
	xorl	%edi, %edi
	call	exit
	.cfi_endproc
.LFE28:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE13:
	.section	.text.startup
.LHOTE13:
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
